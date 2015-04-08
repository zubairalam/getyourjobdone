(function () {
    var app = angular.module('mainApp', ['ui.bootstrap', 'ngMessages']);

    var ForgotPasswordController = function ($scope, $http) {
        var model = this;

        model.user = {
            email: ""
        };

        $scope.alerts = [];

        $scope.closeAlert = function (index) {
            $scope.alerts.splice(index, 1);
        };

        model.submit = function (isValid) {
            if (isValid) {
                $http.post('http://localhost:5000/api/v1/auth/local/forgot', model.user)
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
                        else {
                            if ($scope.alerts.length > 0)
                                $scope.alerts = [];

                            $scope.alerts.push({
                                type: 'success',
                                msg: 'Please check your email for instructions on how to proceed further.'
                            });
                        }

                    })
                    .error(function (data) {
                        // need to do some logging with data.
                        if ($scope.alerts.length > 0)
                            $scope.alerts = [];
                        $scope.alerts.push({
                            type: 'danger',
                            msg: 'Our sincere apologies but we could not email you at the moment. Please try again later.'
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
    app.controller("ForgotPasswordController", ForgotPasswordController);

}());

