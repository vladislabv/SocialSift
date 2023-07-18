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
)
from flask_login import login_required, login_user, logout_user

from gih.extensions import login_manager
from gih.public.forms import LoginForm
from gih.user.forms import RegisterForm
from gih.user.models import User
from gih.utils import flash_errors, get_restaurants

blueprint = Blueprint("public", __name__, static_folder="../static")


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


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
