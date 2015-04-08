(function () {
    var app = angular.module('mainApp', ['ui.bootstrap', 'ngMessages']);

    var LoginController = function ($scope, $http, $window) {
        var model = this;

        model.user = {
            email: "",
            password: ""
        };

        $scope.alerts = [];

        $scope.closeAlert = function (index) {
            $scope.alerts.splice(index, 1);
        };

        model.submit = function (isValid) {
            if (isValid) {
                $http.post('http://localhost:5000/api/v1/auth/local/login', model.user)
                    .success(function (data) {
                        var response = JSON.stringify(data);
                        if (response === '{"message":"user does not exist"}') {
                            if ($scope.alerts.length > 0)
                                $scope.alerts = [];

                            $scope.alerts.push({
                                type: 'danger',
                                msg: 'Sorry, this email address has not been registered with us.'
                            });
                        }

                        else if (response === '{"message":"invalid credentials"}') {
                            if ($scope.alerts.length > 0)
                                $scope.alerts = [];

                            $scope.alerts.push({
                                type: 'danger',
                                msg: 'We have located your account but the password you entered is not valid.'
                            });
                        }
                        else
                        // need checking here if profile wizard has completed or not else redirect to dashboard
                            $window.location.href = '/dashboard';
                    })
                    .error(function (data) {
                        // need to do some logging with data.
                        if ($scope.alerts.length > 0)
                            $scope.alerts = [];
                        $scope.alerts.push({
                            type: 'danger',
                            msg: 'Our sincere apologies but we could not log you in at the moment. Please try again later.'
                        });
                    });
            }
            else {
                if ($scope.alerts.length > 0)
                    $scope.alerts = [];
                $scope.alerts.push({type: 'warning', msg: 'There are still some invalid fields below.'});
            }

        };

    };
    app.controller("LoginController", LoginController);

}());

