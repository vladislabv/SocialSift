// Initialize the map
var map = L.map('map').setView([53.551086, 9.993682], 13); // Set the initial view coordinates and zoom level

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
}).addTo(map);

//var markersLayer;
var neighbourhoodsLayer;
var markersLayer = L.markerClusterGroup(); // L.layerGroup();

function loadNeighbourhoods() {
    var bounds = map.getBounds();
    var neighbourhoodsURL = '/get_neighbourhoods';

    $.ajax({
        url: neighbourhoodsURL,
        type: 'GET',
        data: {
            min_latitude: bounds.getSouthWest().lat,
            min_longitude: bounds.getSouthWest().lng,
            max_latitude: bounds.getNorthEast().lat,
            max_longitude: bounds.getNorthEast().lng
        },
        success: function (data) {
            // Remove existing neighbourhoods layer
            if (neighbourhoodsLayer) {
                map.removeLayer(neighbourhoodsLayer);
            }

            // Add new neighbourhoods layer
            neighbourhoodsLayer = L.geoJSON(data, {
                onEachFeature: function (feature, layer) {

                    var popupContent = `
                        <b>${feature.properties.name}</b><br>
                        Boundary: ${feature.properties.boundary}<br>
                        Popular Cuisines: ${feature.properties.kitchen_types}<br>
                        Avg. Price: ${feature.properties.average_price}<br>
                        Avg. Rating: ${feature.properties.average_rating}<br>
                        Upscale Ratio: ${feature.properties.upscale_ratio}<br>
                    `;
                    layer.bindPopup(popupContent);
                },
                style: function (feature) {
                    return {
                        fillColor: 'grey',
                        fillOpacity: 0.5,
                        color: 'black',
                        weight: 2
                    };
                }
            }).addTo(map);

            // Add markers layer to the neighbourhoods layer
            markersLayer.addTo(neighbourhoodsLayer);
        }
    });
}

// function loadRestaurants () {
//     var bounds = map.getBounds();
//     var min_latitude = bounds.getSouthWest().lat;
//     var min_longitude = bounds.getSouthWest().lng;
//     var max_latitude = bounds.getNorthEast().lat;
//     var max_longitude = bounds.getNorthEast().lng;

//     // Make an AJAX request to get the restaurants within the current view
//     $.ajax({
//         url: '/get_restaurants',
//         type: 'GET',
//         data: {
//             min_latitude: min_latitude,
//             min_longitude: min_longitude,
//             max_latitude: max_latitude,
//             max_longitude: max_longitude
//         },
//         success: function (data) {
//             // Clear existing markers from the layer group
//             markersLayer.clearLayers();

//             // Add new restaurants as markers
//             data.features.forEach(function (feature) {
//                 var coordinates = feature.geometry.coordinates.reverse(); // Reverse the coordinates (Leaflet uses [lat, lng])
//                 var name = feature.properties.name;

//                 var restaurantMarker = L.marker(coordinates)
//                     .bindPopup(
//                         `
//                         <b>${feature.properties.name}</b><br>
//                         Address: ${feature.properties.street}<br>
//                         ZIP: ${feature.properties.zip}<br>
//                         `
//                     ).addTo(markersLayer);
//             });
//         }
//     });
// }

// Function to load restaurants dynamically
function loadRestaurants() {
    var bounds = map.getBounds();
    var restaurantsURL = '/get_restaurants';

    $.ajax({
        url: restaurantsURL,
        type: 'GET',
        data: {
            min_latitude: bounds.getSouthWest().lat,
            min_longitude: bounds.getSouthWest().lng,
            max_latitude: bounds.getNorthEast().lat,
            max_longitude: bounds.getNorthEast().lng
        },
        success: function (data) {
            // Clear existing markers from the layer group
            markersLayer.clearLayers();

            // Add new restaurants as markers
            data.features.forEach(function (feature) {
                var coordinates = feature.geometry.coordinates.reverse(); // Reverse the coordinates (Leaflet uses [lat, lng])

                var popupContent = `
                    <b>${feature.properties.name}</b><br>
                    Address: ${feature.properties.street} ${feature.properties.zip} ${feature.properties.city}<br>
                    Phone: ${feature.properties.phone}<br>
                    Website: <a href="${feature.properties.website}" target="_blank">${feature.properties.website}</a><br>
                    Cuisine: ${feature.properties.kitchen_types}<br>
                    Avg. Price: ${feature.properties.average_price}<br>
                    Avg. Rating: ${feature.properties.average_rating}<br>
                `;

                var restaurantMarker = L.marker(coordinates)
                    .bindPopup(popupContent)
                    .addTo(markersLayer);
            });
        }
    });
}

function loadRestaurantsAndNeighbourhoods() {
    loadRestaurants();
    loadNeighbourhoods();
}

// Set up an event listener to detect when the map view changes
map.on('moveend', loadRestaurantsAndNeighbourhoods);

// Initial load of restaurants and neighbourhoods
loadRestaurantsAndNeighbourhoods();