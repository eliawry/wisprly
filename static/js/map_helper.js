function handleNoGeolocation(errorFlag, map) {
        if (errorFlag) {
          var content = 'Error: The Geolocation service failed.';
        } else {
          var content = 'Error: Your browser doesn\'t support geolocation.';
        }

        var options = {
          map: map,
          position: new google.maps.LatLng(30.16, -97.44),
          content: content
        };

        var infowindow = new google.maps.InfoWindow(options);
        map.setCenter(options.position);
}


var styles = [
      {
          stylers: [
            { hue: "#00ffe6" },
            { saturation: -20 }
          ]
        },{
          featureType: "road",
          elementType: "geometry",
          stylers: [
            { lightness: 100 },
            { visibility: "simplified" }
          ]
        },{
          featureType: "road",
          elementType: "labels",
          stylers: [
            { visibility: "off" }
          ]
        }
      ];

function attachMessage(marker, path) {
       var boxText = document.createElement("div");
        boxText.style.cssText = "margin-top: 2px; background: #8FC4BC; padding: 2px; border-radius: 70px;";

       boxText.innerHTML ='<iframe width="250" height="250" src="' + path + '" frameborder="0" allowfullscreen></iframe>';

        var myOptions = {
                 content: boxText
                ,disableAutoPan: false
                ,maxWidth: 0
                ,pixelOffset: new google.maps.Size(-140, 0)
                ,zIndex: null
                ,boxStyle: { 
                  opacity: 1
                 }
                ,closeBoxMargin: "2px 2px 2px 2px"
                ,closeBoxURL: "http://www.google.com/intl/en_us/mapfiles/close.gif"
                ,infoBoxClearance: new google.maps.Size(1, 1)
                ,isHidden: false
                ,pane: "floatPane"
                ,enableEventPropagation: false
        };

        var ib = new InfoBox(myOptions);
        google.maps.event.addListener(marker, 'click', function() {
          ib.open(marker.get('map'), marker);
        });
}

function clearOverlays(markersArray) {
  for (var i = 0; i < markersArray.length; i++ ) {
    markersArray[i].setMap(null);
  }
  markersArray = [];
}