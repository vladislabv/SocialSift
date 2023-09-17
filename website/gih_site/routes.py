from flask import render_template, request, jsonify
from gih_site import app
from pymongo import MongoClient
import shapely

# Connect to your MongoDB instance
client = MongoClient('mongodb+srv://vstasenko:G3DL45JpkEnSN0ry@gastrohub.o9izr0g.mongodb.net/')
db = client['web_scraper']
collection = db['restos']

@app.route('/')
def index():
    return render_template('public/test.html')

@app.route('/get_restaurants', methods=['GET'])
def get_restaurants():
    # Retrieve the current view bounds from the frontend (latitude, longitude, zoom level)
    # Use these values to query the database for restaurants within the bounds
    # Return the restaurants as GeoJSON
    min_latitude = request.args.get('min_latitude', type=float)
    min_longitude = request.args.get('min_longitude', type=float)
    max_latitude = request.args.get('max_latitude', type=float)
    max_longitude = request.args.get('max_longitude', type=float)

    # neighbourhood_id = request.args.get('neighbourhood_id')
    # Make sure the 'location' field is properly formatted as GeoJSON Point

    # Example code:
    restaurants = db["view_restos"].find({
        'location': {
            '$geoWithin': {
                '$box': [
                    [min_longitude, min_latitude],
                    [max_longitude, max_latitude]
                ]
            }
        }
    })

    # restaurants = collection.find({
    #     'neighbourhood_id': neighbourhood_id
    # }, {'_id': 0})
    
    geojson_restaurants = {
        "type": "FeatureCollection",
        "features": []
    }

    for restaurant in restaurants:
        if not restaurant.get('location'):
            continue

        if not restaurant.get('name'):
            continue

        if not restaurant.get('address'):
            restaurant["address"] = {}

        avg_price = restaurant.get("average_price")
        if not isinstance(avg_price, str):
            avg_price = str(round(avg_price, 2)) + " €"

        avg_rating = restaurant.get("average_rating")
        if not isinstance(avg_rating, str):
            avg_rating = str(round(avg_rating, 2)) + " ⭐"

        geojson_restaurants["features"].append({
            "type": "Feature",
            "geometry": restaurant['location'],
            "properties": {
                "name": restaurant["name"],
                "street": restaurant["address"].get("street", ""),
                "zip": restaurant["address"].get("zip", ""),
                "city": restaurant["address"].get("city", ""),
                "phone": restaurant.get("phone", ""),
                "website": restaurant.get("website", ""),
                "kitchen_types": restaurant.get("kitchen_types", "").lower(),
                "average_price": avg_price,
                "average_rating": avg_rating
            }
        })

    return jsonify(geojson_restaurants)


@app.route('/get_neighbourhoods', methods=['GET'])
def get_neighbourhoods():
    min_latitude = request.args.get('min_latitude', type=float)
    min_longitude = request.args.get('min_longitude', type=float)
    max_latitude = request.args.get('max_latitude', type=float)
    max_longitude = request.args.get('max_longitude', type=float)

    # Define the bounding box as a Polygon
    bounding_box = {
        "type": "Polygon",
        "coordinates": [
            [
                [min_longitude, min_latitude],
                [max_longitude, min_latitude],
                [max_longitude, max_latitude],
                [min_longitude, max_latitude],
                [min_longitude, min_latitude]
            ]
        ]
    }

    # Use these values to query your MongoDB for neighborhoods within the bounds
    # Example:
    # Convert the bounding box to a Shapely geometry
    # bounding_box_shape = shapely.geometry.shape(bounding_box)
    MAX_TRIES = 3
    for i in range(MAX_TRIES):
        # Find neighborhoods that intersect with the bounding box
        neighbourhoods = db["view_neighbourhoods"].find({
            'neighbourhood.geometry': {
                '$geoIntersects': {
                    '$geometry': bounding_box
                }
            }
        })
        neighbourhoods = list(neighbourhoods)
        if len(neighbourhoods) > 0:
            break

        import time
        time.sleep(1)

    geojson_neighbourhoods = {
        "type": "FeatureCollection",
        "features": []
    }

    for neighbourhood in neighbourhoods:

        if not neighbourhood.get('neighbourhood'):
            continue

        avg_price = neighbourhood.get("average_price_glob")
        if not isinstance(avg_price, str):
            avg_price = str(round(avg_price, 2)) + " €"

        avg_rating = neighbourhood.get("average_rating_glob")
        if not isinstance(avg_rating, str):
            avg_rating = str(round(avg_rating, 2)) + " ⭐"

        upscale_ratio = neighbourhood.get("upscale_ratio")
        if not isinstance(upscale_ratio, str):
            upscale_ratio = str(round(upscale_ratio, 2) * 100) + " %"

        geojson_neighbourhoods["features"].append({
            "type": "Feature",
            "geometry": neighbourhood['neighbourhood']['geometry'],
            "properties": {
                "name": neighbourhood['neighbourhood'].get("properties", {}).get("name", "Unknown"),
                "boundary": neighbourhood['neighbourhood'].get("properties", {}).get("boundary", "Unknown"),
                "kitchen_types": neighbourhood.get("top_kitchen_types", "Unspecified"),
                "average_price": avg_price,
                "average_rating": avg_rating,
                "upscale_ratio": upscale_ratio
            }
        })

    return jsonify(geojson_neighbourhoods)