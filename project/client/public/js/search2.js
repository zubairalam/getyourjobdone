(function () {
    var app = angular.module('mainApp', []);
    var SearchController = function ($scope, $http) {
        //$http.get('http://localhost:5000/api/v1/countries?select=name')
        //.success(function (response) {
        //    $scope.countries = response;
        //});
    };
     app.controller("SearchController", SearchController);

}());
