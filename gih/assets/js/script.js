// App initialization code goes here

// FUNCTIONS
// function onMapClick(e) {
//     var popup = L.popup();
//     popup
//         .setLatLng(e.latlng)
//         .setContent("You clicked the map at " + e.latlng.toString())
//         .openOn(map);
// }

function moveCircle(e) {
    map.setView([e.latlng.lat, e.latlng.lng], map.getZoom()); //last is zoom level
    if ( map.hasLayer(circle) ) {
        //Start
        circle.setLatLng(e.latlng);
        //End
    } else {
        L.Circle([e.latlng.lat, e.latlng.lng], 500).addTo(map);
    }
}

function load_slider_data() {
    var input = document.getElementById("DistanceRange");
    if(localStorage.getItem("server") != null){
        input.value = localStorage.getItem("server");
        document.getElementById("DistanceValue").innerHTML = slider.value;
    }
}

window.addEventListener("DOMContentLoaded", (event) => {
    if (typeof map != "undefined") {
        L.geoJSON(
            'static/build/comp_plz.geojson', 
            {
                style: function (feature) {
                    return {color: feature.properties.color};
                },
                onEachFeature: function (feature, layer) {
                    layer.bindPopup(feature.properties.PCON13NM);
                }
            }
        ).addTo(map);
        map.on('click', moveCircle);
    }
});

// SLIDER
var slider = document.getElementById("DistanceRange");
var output = document.getElementById("DistanceValue");
output.innerHTML = slider.value;

slider.oninput = function() {
    output.innerHTML = this.value;
    save_data();
};

if (slider && output) {
    output.innerHTML = slider.value;
    slider.oninput = function() {
        if ( typeof circle != "undefined" ) {
            circle.setRadius( parseInt(this.value) * 1000 );
            save_slider_data();
        }
        output.innerHTML = this.value + " km";
    }
    load_slider_data();
}