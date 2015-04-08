(function () {
    var app = angular.module('mainApp', ['ui.bootstrap',
        'ngMessages'
        //'uiGmapgoogle-maps' commented as we're not showing maps anymore.
        ]
    );
    var EnquiryController = function ($scope, $http) {
        var model = this;

        model.enquiry = {
            firstName: "",
            lastName: "",
            email: "",
            subject: "",
            description: ""
        };
        $scope.alerts = [];
        $scope.closeAlert = function (index) {
            $scope.alerts.splice(index, 1);
        };
        model.submit = function (isValid) {
            if (isValid) {
                $http.post('http://localhost:5000/api/v1/enquiries', model.enquiry)
                    .success(function (data) {
                        $scope.alerts.push({
                            type: 'success',
                            msg: 'Thank you for contacting us. Your query has reached us safely. We\'ll be in touch soon'
                        });
                    })
                    .error(function (data) {
                        // need to do some logging with data.
                        if ($scope.alerts.length > 0)
                            $scope.alerts = [];
                        $scope.alerts.push({
                            type: 'danger',
                            msg: 'Sorry, we could not register you at this time.'
                        });
                    });
            }
            else {
                if ($scope.alerts.length > 0)
                    $scope.alerts = [];
                $scope.alerts.push({
                    type: 'warning',
                    msg: 'There are still some invalid fields.'
                });
            }

        };
    };


    //app.config(function (uiGmapGoogleMapApiProvider) {
    //    uiGmapGoogleMapApiProvider.configure({
    //        //    key: 'your api key',
    //        v: '3.17',
    //        libraries: 'weather,geometry,visualization'
    //    });
    //});

    //var MapController = function ($scope, uiGmapGoogleMapApi) {
    //    uiGmapGoogleMapApi.then(function (maps) {
    //        $scope.map = {
    //            center: {
    //                latitude: 51.523516,
    //                longitude: -0.102726
    //            },
    //            zoom: 12,
    //            bounds: {}
    //        };
    //        $scope.options = {
    //            scrollwheel: false
    //        };
    //        $scope.marker = {
    //            id: 0,
    //            coords: {
    //                latitude: 51.523516,
    //                longitude: -99.6680
    //            },
    //            options: {draggable: true},
    //            events: {
    //                dragend: function (marker, eventName, args) {
    //                    $log.log('marker dragend');
    //                    var lat = marker.getPosition().lat();
    //                    var lon = marker.getPosition().lng();
    //                    $log.log(lat);
    //                    $log.log(lon);
    //
    //                    $scope.marker.options = {
    //                        draggable: true,
    //                        labelContent: "lat: " + $scope.marker.coords.latitude + ' ' + 'lon: ' + $scope.marker.coords.longitude,
    //                        labelAnchor: "100 0",
    //                        labelClass: "marker-labels"
    //                    };
    //                }
    //            }
    //        };
    //
    //    });
    //
    //};
    //app.controller("MapController", MapController);
    app.controller("EnquiryController", EnquiryController);
}());

