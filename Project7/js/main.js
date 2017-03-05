$(document).ready(function() {
    var LocData = [{
            "name": "The Beer Cafe",
            "location": [28.629144, 77.2176282]
        },
        {
            "name": "Monkey Bar",
            "location": [28.63154144442592, 77.2163011815591]
        },
        {
            "name": "Route 04",
            "location": [28.634879682422973, 77.22027719020844]
        },
        {
            "name": "MyBar Headquarters",
            "location": [28.63159614132705, 77.21993347329604]
        },
        {
            "name": "Farzi Cafe",
            "location": [28.632583358124705, 77.22120783667748]
        }
    ];



    var mapModel = function() {
        var self = this;
        self.search = ko.observable("");
        self.allLocations = ko.observableArray([]);
        self.markers = ko.observableArray([]);
        self.filter = ko.observable("");

        var map = mapLoad();
        if (map == null) {
            console.log("Error Loading Map!");
            return;
        }
        self.map = ko.observable(map);
        getplacesFs(self.allLocations, self.map(), self.markers);
        self.filteredArray = ko.computed(function() {
            return ko.utils.arrayFilter(self.allLocations(), function(item) {
                if (item.name.toLowerCase().indexOf(self.filter().toLowerCase()) !== -1) {
                    if (item.marker != null)
                        item.marker.setMap(map);
                } else {
                    if (item.marker)
                        item.marker.setMap(null);
                }
                return item.name.toLowerCase().indexOf(self.filter().toLowerCase()) !== -1;
            });
        }, self);

        self.clickHandler = function(data) {
            mapCenter(data, self.map(), self.markers);
        };
    };

    /*
    Taken from: 
    https://developers.google.com/maps/documentation/javascript/examples/marker-animations
    */

    function animateMarker(marker) {

        if (marker.setAnimation() == null) {
            marker.setAnimation(google.maps.Animation.BOUNCE);
            setTimeout(function() {
                marker.setAnimation(null);
            }, 720);
        } else {
            marker.setAnimation(null);
        }
    }

    function mapLoad() {
        var mapsettings = {
            center: new google.maps.LatLng(28.634879682422973, 77.22027719020844),
            zoom: 15,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        return new google.maps.Map(document.getElementById('canvas-view'), mapsettings);
    }

    function getplacesFs(allLocations, map, markers) {
        var location = [];
        var locdata = [];
        for (var loc in LocData) {
            baseuUrl = 'https://api.foursquare.com/v2/venues/search'
            var foursquareUrl = baseuUrl +
                '?client_id=MKFNW4NXFI5M4D0E44ZKSL4RGD0UOGVTYZQHNMCNSNNQMQGR' +
                '&client_secret=X3QTZOQ3RWQ2BVLDG50LHMSUCFX54TCPVGCJ40RVMAEYCNKB' +
                '&m=foursquare' +
                '&v=20161507' +
                '&query=' + LocData[loc]["name"] +
                '&ll=' + LocData[loc]["location"][0] + ',' + LocData[loc]["location"][1] +
                '&intent=match';

            $.getJSON(foursquareUrl, function(data) {
                if (data.response.venues) {
                    var item = data.response.venues[0];
                    allLocations.push(item);
                    location = {
                        lat: item.location.lat,
                        lng: item.location.lng,
                        name: item.name,
                        loc: item.location.address + " " + item.location.city + ", " + item.location.state + " " + item.location.postalCode
                    };
                    locdata.push(location);
                    setMarkers(allLocations, loc, location, map, markers);
                } else {
                    console.log("Error!! Couldn't find data ");
                    return;
                }
            });
        }
    }


    /*
      Taken from: 
      https://developers.google.com/maps/documentation/javascript/examples/marker-animations
      */


    function setMarkers(allLocations, loc, data, map, markers) {
        var latlng = new google.maps.LatLng(data.lat, data.lng);
        var marker = new google.maps.Marker({
            position: latlng,
            map: map,
            animation: google.maps.Animation.DROP,
            content: data.name + "<br>" + data.loc
        });
        var infoWindow = new google.maps.InfoWindow({
            content: marker.content
        });
        marker.infowindow = infoWindow;
        markers.push(marker);
        allLocations()[allLocations().length - 1].marker = marker;

        google.maps.event.addListener(marker, 'click', function() {
            for (var i = 0; i < markers().length; i++) {
                markers()[i].infowindow.close();
            }
            infoWindow.open(map, marker);
        });

        google.maps.event.addListener(marker, 'click', function() {
            animateMarker(marker);
        });

    }

    ko.applyBindings(new mapModel());
});