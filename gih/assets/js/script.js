// App initialization code goes here

// FUNCTIONS
function onMapClick(e) {
    var popup = L.popup();
    popup
        .setLatLng(e.latlng)
        .setContent("You clicked the map at " + e.latlng.toString())
        .openOn(map);
}

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

window.addEventListener("DOMContentLoaded", (event) => {
    if (typeof map != "undefined") {
        map.on('click', onMapClick);
        map.on('click', moveCircle);
    }
});

// SLIDER
var slider = document.getElementById("DistanceRange");
var output = document.getElementById("DistanceValue");
if (slider && output) {
    output.innerHTML = slider.value;
    slider.oninput = function() {
        if ( typeof circle != "undefined" ) {
            circle.setRadius( parseInt(this.value) * 1000 );
        }
        output.innerHTML = this.value + " km";
    }
}