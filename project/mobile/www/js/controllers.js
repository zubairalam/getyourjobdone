angular.module('starter.controllers', ['ng-cordova'])

    .controller('HomeCtrl', function ($scope) {
    })

    .controller('ConnectionsCtrl', function ($scope, Connections) {
        $scope.connections = Connections.all();
    })

    .controller('ConnectionDetailCtrl', function ($scope, $stateParams, Connections) {
        $scope.connection = Connections.get($stateParams.connectionId);
    })

    .controller('JobsCtrl', function ($scope, Jobs) {
        $scope.jobs = Jobs.all();
    })

    .controller('JobDetailCtrl', function ($scope, $stateParams, Jobs) {
        $scope.job = Jobs.get($stateParams.jobId);
    })

    .controller('AccountCtrl', function ($scope) {
    });
