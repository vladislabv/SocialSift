GET_RESTAURANTS = [
    {
        '$unwind': {
            'path': '$menu_positions', 
            'preserveNullAndEmptyArrays': False
        }
    }, {
        '$unwind': {
            'path': '$reviews', 
            'preserveNullAndEmptyArrays': False
        }
    }, {
        '$group': {
            '_id': '$_id', 
            'name': {
                '$first': '$name'
            }, 
            'website': {
                '$first': '$website'
            }, 
            'kitchen_types': {
                '$first': '$kitchen_types'
            }, 
            'phone': {
                '$first': '$phone'
            }, 
            'address': {
                '$first': '$address'
            }, 
            'location': {
                '$first': '$location'
            }, 
            'neighbourhood_id': {
                '$first': '$neighbourhood_id'
            }, 
            'average_price': {
                '$avg': '$menu_positions.price'
            }, 
            'average_rating': {
                '$avg': '$reviews.rating'
            }
        }
    }, {
        '$project': {
            '_id': 0, 
            'name': {
                '$trim': {
                    'input': '$name'
                }
            }, 
            'website': 1, 
            'kitchen_types': 1, 
            'phone': 1, 
            'address': 1, 
            'location': 1, 
            'neighbourhood_id': 1, 
            'average_price': {
                '$ifNull': [
                    '$average_price', 'Unspecified'
                ]
            }, 
            'average_rating': {
                '$ifNull': [
                    '$average_rating', 'Unspecified'
                ]
            }
        }
    }
]

GET_NEIGHBOURHOODS = [
    {
        '$lookup': {
            'from': 'neighbourhoods_test', 
            'localField': 'neighbourhood_id', 
            'foreignField': '_id', 
            'as': 'neighbourhood'
        }
    }, {
        '$unwind': {
            'path': '$neighbourhood', 
            'preserveNullAndEmptyArrays': False
        }
    }, {
        '$project': {
            '_id': 0, 
            'kitchen_types': 1, 
            'neighbourhood': 1, 
            'average_price': 1, 
            'average_rating': 1, 
            'kitchen_types': 1
        }
    }, {
        '$group': {
            '_id': '$neighbourhood._id', 
            'average_price_glob': {
                '$avg': '$average_price'
            }, 
            'average_rating_glob': {
                '$avg': '$average_rating'
            }, 
            'neighbourhood': {
                '$first': '$neighbourhood'
            }, 
            'kitchen_types': {
                '$push': {
                    '$toLower': '$kitchen_types'
                }
            }, 
            'restos_count': {
                '$sum': 1
            }, 
            'restos_count_upscale': {
                '$sum': {
                    '$cond': [
                        {
                            '$gte': [
                                '$average_price', 50
                            ]
                        }, 1, 0
                    ]
                }
            }
        }
    }, {
        '$unwind': {
            'path': '$kitchen_types', 
            'preserveNullAndEmptyArrays': False
        }
    }, {
        '$group': {
            '_id': {
                'neighbourhood_id': '$neighbourhood._id', 
                'kitchen_type': '$kitchen_types'
            }, 
            'neighbourhood': {
                '$first': '$neighbourhood'
            }, 
            'average_price_glob': {
                '$first': '$average_price_glob'
            }, 
            'average_rating_glob': {
                '$first': '$average_rating_glob'
            }, 
            'restos_count': {
                '$first': '$restos_count'
            }, 
            'restos_count_upscale': {
                '$first': '$restos_count_upscale'
            }, 
            'count': {
                '$sum': 1
            }
        }
    }, {
        '$sort': {
            'count': -1
        }
    }, {
        '$group': {
            '_id': '$_id.neighbourhood_id', 
            'neighbourhood': {
                '$first': '$neighbourhood'
            }, 
            'average_price_glob': {
                '$first': '$average_price_glob'
            }, 
            'average_rating_glob': {
                '$first': '$average_rating_glob'
            }, 
            'restos_count': {
                '$first': '$restos_count'
            }, 
            'restos_count_upscale': {
                '$first': '$restos_count_upscale'
            }, 
            'top_kitchen_types': {
                '$push': {
                    'kitchen_type': '$_id.kitchen_type', 
                    'count': '$count'
                }
            }
        }
    }, {
        '$addFields': {
            'upscale_ratio': {
                '$divide': [
                    '$restos_count_upscale', '$restos_count'
                ]
            }, 
            'top_kitchen_types': {
                '$reduce': {
                    'input': {
                        '$slice': [
                            '$top_kitchen_types', 3
                        ]
                    }, 
                    'initialValue': '', 
                    'in': {
                        '$concat': [
                            '$$value', {
                                '$ifNull': [
                                    ', ', ''
                                ]
                            }, '$$this.kitchen_type'
                        ]
                    }
                }
            }
        }
    }, {
        '$project': {
            '_id': 0, 
            'neighbourhood': 1, 
            'upscale_ratio': 1, 
            'average_price_glob': 1, 
            'average_rating_glob': 1, 
            'top_kitchen_types': {
                '$trim': {
                    'input': '$top_kitchen_types', 
                    'chars': ', '
                }
            }
        }
    }
]