from itemadapter import ItemAdapter
import pymongo

class ProcessMongoEntries:
    item = None
    spider = None
    
    @classmethod
    def websites(cls, item, spider, collection):
        d = ItemAdapter(item).asdict()
        collection.insert_one(d)
        return
    
    @classmethod
    def restos(cls, item, spider, db, collection):
        d = ItemAdapter(item).asdict()
        # swap restos coordinates
        try:
            d["location"]["coordinates"].reverse()
        except KeyError:
            pass

        # pinpoint the corresponding neighbourhood
        neighborhood = db['neighbourhoods_test'].find_one(
            { "geometry" : { "$geoIntersects": {"$geometry": d["location"] } } }
        )
        if neighborhood:
            d["neighbourhood_id"] = neighborhood["_id"]

        # first insert all menu positions // reference them in the resto
        menu_positions = d.pop("menu_positions", [])
        if len(menu_positions) > 0:
            r = db["menus"].insert_many(menu_positions)
            # reference inserted ids in the resto collection
            d["menu_position_ids"] = r.inserted_ids

        # first insert all reviews // reference them in the resto
        reviews = d.pop("reviews", [])
        if len(reviews) > 0:
            r = db["reviews"].insert_many(reviews)

            # reference inserted ids in the resto collection
            d["review_ids"] = r.inserted_ids

        try:
            db[collection].insert_one(d)
        except pymongo.errors.DuplicateKeyError as e:
            print("Duplicate key error!")
            print(e)
            print("Trying to update the item...")
            db[collection].replace_one({ "$and": [ {"name": d["name"]}, {"address.street": d["address"].get("street", "")} ] }, d, upsert=True)

        print("Inserted new item!")
        return
    
    def reviews(cls, item, spider, db, collection):
        d = ItemAdapter(item).asdict()
        name = d.pop("resto_name", "")
        city = d.pop("resto_city", "")
        if name and city:
            r = db[collection].insert_one(d)
            try:
                # append review to the restaurant
                db["restos"].update_one(
                    {
                        "$and": [
                            {"name": name},
                            {"adress.city": city}
                        ]
                    },
                    {"$push": {"review_ids": r.inserted_id}}
                )
            except Exception as e:
                print(e)
        return

