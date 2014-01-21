
    var map;
    var geocoder = new google.maps.Geocoder();

    /*function initialize() {
        var latlng = new google.maps.LatLng(34.02109014442118, -118.41173249999997);
        var myOptions = {
            zoom: 10,
            center: latlng,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);

        createMarker(latlng);

    }*/

    function geocode() {
        var address = document.getElementById("address").value;
        geocoder.geocode({
            'address': address,
            'partialmatch': true}, geocodeResult);
    }

    function createMarker(latlng){
        marker = new google.maps.Marker({
            position: latlng,
            map: map,
            draggable: true
        });

        // Update current position info.
        updateMarkerPosition(latlng);
        geocodePosition(latlng);

        google.maps.event.addListener(marker, 'drag', function() {
            updateMarkerPosition(marker.getPosition());
        });

        google.maps.event.addListener(marker, 'dragend', function() {
            geocodePosition(marker.getPosition());
        });

        google.maps.event.addListener(map, 'click', function(event) {
            marker.setMap(null);
            createMarker(event.latLng);
        });
    }

    function geocodeResult(results, status) {
        if (status == 'OK' && results.length > 0) {
            map.fitBounds(results[0].geometry.viewport);
            var latlng = results[0].geometry.location;
            marker.setMap(null);
            createMarker(latlng);
        } else {
            alert("Geocode was not successful for the following reason: " + status);
        }
    }

    function geocodePosition(pos) {
        geocoder.geocode({
            latLng: pos
        },
        function(responses) {
            if (responses && responses.length > 0) {
                updateMarkerAddress(responses[0].formatted_address);
            } else {
                updateMarkerAddress('Cannot determine address at this location.');
            }
        });
    }

    function updateMarkerPosition(latLng) {
        document.getElementById('latlng').value = [
            latLng.lat(),
            latLng.lng()
        ].join(', ');
        document.getElementById('ll').innerHTML = [
            latLng.lat(),
            latLng.lng()
        ].join(', ');
    }

    function updateMarkerAddress(str) {
        document.getElementById('formatedAddress').value = str;
        document.getElementById('fa').innerHTML = str;
    }

    //google.maps.event.addDomListener(window, 'load', initialize);


