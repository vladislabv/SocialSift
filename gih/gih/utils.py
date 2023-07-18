# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from flask import flash
import overpy


def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{getattr(form, field).label.text} - {error}", category)

# OPEN STREET MAP HELPERS
def get_restaurants(latitude, longitude, c_radius):
    # Initialize the API
    api = overpy.Overpass()
    # Define the query
    query = """(node["amenity"="restaurant"](around:{radius},{lat},{lon});
                node["amenity"="cafe"](around:{radius},{lat},{lon});
            );out;
            """.format(lat=latitude, lon=longitude, radius=c_radius)
    # Call the API
    result = api.query(query)
    return result
