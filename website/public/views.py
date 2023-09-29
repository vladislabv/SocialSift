# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    jsonify,
)
from flask_login import login_required, login_user, logout_user

from website.extensions import login_manager
from website.database import db, db_scraper
from website.public.forms import LoginForm
from website.user.forms import RegisterForm
from website.user.models import User
from website.utils import flash_errors

blueprint = Blueprint("public", __name__, static_folder="../static")


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(user_id)


@blueprint.route("/", methods=["GET", "POST"])
@blueprint.route("/home/", methods=["GET", "POST"])
def home():
    """Home page."""
    form = LoginForm(request.form)
    current_app.logger.info("Hello from the home page!")
    # Handle logging in
    if request.method == "POST":
        if form.validate_on_submit():
            login_user(form.user)
            flash("You are logged in.", "success")
            redirect_url = request.args.get("next") or url_for("user.members")
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template("public/home.html", form=form)


@blueprint.route("/logout/")
@login_required
def logout():
    """Logout."""
    logout_user()
    flash("You are logged out.", "info")
    return redirect(url_for("public.home"))


@blueprint.route("/register/", methods=["GET", "POST"])
def register():
    """Register new user."""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        User.create(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            active=True,
        )
        flash("Thank you for registering. You can now log in.", "success")
        return redirect(url_for("public.home"))
    else:
        flash_errors(form)
    return render_template("public/register.html", form=form)


@blueprint.route("/about/")
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template("public/about.html", form=form)


@blueprint.route('/get_restaurants', methods=['GET'])
def get_restaurants():
    # Retrieve the current view bounds from the frontend (latitude, longitude, zoom level)
    # Use these values to query the database for restaurants within the bounds
    # Return the restaurants as GeoJSON
    min_latitude = request.args.get('min_latitude', type=float)
    min_longitude = request.args.get('min_longitude', type=float)
    max_latitude = request.args.get('max_latitude', type=float)
    max_longitude = request.args.get('max_longitude', type=float)

    # Make sure the 'location' field is properly formatted as GeoJSON Point
    restaurants = db_scraper["view_restos"].find({
        'location': {
            '$geoWithin': {
                '$box': [
                    [min_longitude, min_latitude],
                    [max_longitude, max_latitude]
                ]
            }
        }
    })
    
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


@blueprint.route('/get_neighbourhoods', methods=['GET'])
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
    MAX_TRIES = 3
    for i in range(MAX_TRIES):
        # Find neighborhoods that intersect with the bounding box
        neighbourhoods = db_scraper["view_neighbourhoods"].find({
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


@blueprint.route('/map/', methods=['GET', 'POST'])
def map():
    """Map page."""
    markers = ''
    # Set default view to Berlin City Center
    lat = request.form.get('lat', 52.473197)
    lon = request.form.get('lon', 13.401258)
    c_radius = request.form.get('c_radius', 5000)
    circle_dict = {
        'radius': c_radius,
        'color': 'red',
        'fillColor': '#f03',
        'fillOpacity': 0.5
    }

    circle = "var circle = L.circle([{lat}, {lon}], {circle_dict}).addTo(map);".format(
        lat=lat,
        lon=lon,
        circle_dict=circle_dict
    )

    if request.method == "POST":
        # The code here determines what happens after sumbitting the form

        # collect chosen radius and lat/lon of the circle center
        # this data will be used for looking over the db table
        # with found restaurants metadata and connect the coordinates with the chosen range
        pass
        
    # Get restaurants data from OpenStreetMap
    # restos = get_restaurants(lat, lon, c_radius)

    # Initialize variables
    id_counter = 0

    for node in []: #restos.nodes:
        # Create unique ID for each marker
        idd = 'restaurant' + str(id_counter)
        id_counter += 1

        # Check if shops have name and website in OSM
        resto_brand = node.tags.get('brand')
        resto_website = node.tags.get('website')

        if resto_brand and resto_website:
            # Create the marker and its pop-up for each shop
            markers += "var {idd} = L.marker([{latitude}, {longitude}]);\n\t{idd}.addTo(map).bindPopup('{brand}<br>{website}');\n\n\t".format(
                idd=idd,
                latitude=node.lat,
                longitude=node.lon,
                brand=resto_brand,
                website=resto_website
            )

    # Render the map form
    return render_template('public/map.html', markers=markers, circle=circle, lat=lat, lon=lon, zoom = 10)
