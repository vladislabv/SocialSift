// Initialize the map
var map = L.map('map').setView([53.551086, 9.993682], 13); // Set the initial view coordinates and zoom level

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
}).addTo(map);

var neighbourhoodsLayer;
var restaurantsLayer = L.layerGroup();

function loadNeighbourhoods() {
    var bounds = map.getBounds();

    $.ajax({
        url: '/get_neighbourhoods',
        type: 'GET',
        data: {
            min_latitude: bounds.getSouthWest().lat,
            min_longitude: bounds.getSouthWest().lng,
            max_latitude: bounds.getNorthEast().lat,
            max_longitude: bounds.getNorthEast().lng
        },
        success: function (data) {
            if (neighbourhoodsLayer) {
                map.removeLayer(neighbourhoodsLayer);
            }

            neighbourhoodsLayer = L.geoJSON(data, {
                style: function (feature) {
                    return {
                        fillColor: 'blue',
                        fillOpacity: 0.5,
                        color: 'black',
                        weight: 1
                    };
                },
                onEachFeature: function (feature, layer) {
                    loadRestaurantsInNeighbourhood(feature.properties.neighbourhood_id);
                }
            }).addTo(map);
        }
    });
}

function loadRestaurantsInNeighbourhood(neighbourhood_id) {
    var restaurantsURL = '/get_restaurants_in_neighbourhood';

    $.ajax({
        url: restaurantsURL,
        type: 'GET',
        data: {
            neighbourhood_id: neighbourhood_id
        },
        success: function (data) {
            // Clear existing markers for this neighbourhood
            restaurantsLayer.eachLayer(function (layer) {
                if (layer.feature.properties.neighbourhood_id === neighbourhood_id) {
                    restaurantsLayer.removeLayer(layer);
                }
            });

            // Add new restaurants as markers
            data.features.forEach(function (feature) {
                var coordinates = feature.geometry.coordinates.reverse();
                var name = feature.properties.name;

                var restaurantMarker = L.marker(coordinates)
                    .bindPopup(name)
                    .addTo(restaurantsLayer);
            });
        }
    });
}

// Set up an event listener to detect when the map view changes
map.on('moveend', loadNeighbourhoods);

// Initial load of neighbourhoods
loadNeighbourhoods();