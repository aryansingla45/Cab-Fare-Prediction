function initMap() {
    const mapDiv = document.getElementById("map");
    const map = new google.maps.Map(mapDiv, {
        center: { lat: 40.7128, lng: -74.0060 }, // New York City coordinates
        zoom: 12 // Adjust zoom level as needed
    });

    // Initialize draggable markers for pickup and dropoff locations
    const pickupMarker = new google.maps.Marker({
        position: { lat: 40.7128, lng: -74.0060 }, // Default pickup location (New York City)
        map: map,
        draggable: true,
        title: 'Pickup Location'
    });

    const dropoffMarker = new google.maps.Marker({
        position: { lat: 40.7128, lng: -74.0060 }, // Default dropoff location (New York City)
        map: map,
        draggable: true,
        title: 'Dropoff Location'
    });

    // Event listener for when the pickup marker is dragged
    pickupMarker.addListener('dragend', function(event) {
        document.getElementById('pickup_latitude').value = event.latLng.lat();
        document.getElementById('pickup_longitude').value = event.latLng.lng();
    });

    // Event listener for when the dropoff marker is dragged
    dropoffMarker.addListener('dragend', function(event) {
        document.getElementById('dropoff_latitude').value = event.latLng.lat();
        document.getElementById('dropoff_longitude').value = event.latLng.lng();
    });
}

// Load the Google Maps API script
function loadMapScript() {
    const script = document.createElement("script");
    script.src = "https://maps.googleapis.com/maps/api/js?key=AIzaSyApb69fNQll1kFrfUP-xTIrrOC6xz2MDxA&callback=initMap";
    script.defer = true;
    script.async = true;  // Ensure it loads asynchronously
    document.head.appendChild(script);
}


// Call the function to load the Google Maps API
loadMapScript();