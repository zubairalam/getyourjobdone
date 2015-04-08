(function () {
    var app = angular.module('mainApp', ['ui.bootstrap', 'ngMessages', 'ngCookies']);

    var RegistrationController = function ($scope, $http, $window,$cookieStore) {
        var model = this;

        model.user = {
            email: "",
            firstName: "",
            lastName: "",
            accountType: "",
            password: "",
            confirmPassword: ""
        };

        $scope.alerts = [];

        $scope.closeAlert = function (index) {
            $scope.alerts.splice(index, 1);
        };
        model.submit = function (isValid) {
            if (isValid) {
                $http.post('http://localhost:5000/api/v1/users', model.user)
                    .success(function (data) {


                        // send email verification mail
                        $http.post('http://localhost:5000/api/v1/send-email-verification', {token: data.token})
                            .success(function (data) {
                                if (undefined !== data) {
                                    /* show a notification on wizard that email verification is sent */
                                    console.log(data);
                                }
                            })
                            .error(function (data) {
                                /* show some error notification */
                                console.log(data);
                            });


                        // need checking here if profile wizard has completed or not else redirect to dashboard
                        $cookieStore.put('jp_token', data.token);
                        $cookieStore.put('jp_id', data._id);
                        if (data.accountType === "business") {
                            $window.location.href = "/cp-wizard";
                        } else {
                            $window.location.href = '/profile-wizard';
                        }


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

    var compareTo = function () {
        return {
            require: "ngModel",
            scope: {
                otherModelValue: "=compareTo"
            },
            link: function (scope, element, attributes, ngModel) {

                ngModel.$validators.compareTo = function (modelValue) {
                    return modelValue == scope.otherModelValue;
                };

                scope.$watch("otherModelValue", function () {
                    ngModel.$validate();
                });
            }
        };
    };

    app.directive("compareTo", compareTo);
    app.controller("RegistrationController", RegistrationController);

}());

