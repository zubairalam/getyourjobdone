(function () {
    var app = angular.module('mainApp', ['ui.bootstrap', 'notificationsBar', 'ngSanitize']);

    var NavBarController = function ($scope) {
        $scope.status = {
            isopen: false
        };

        $scope.toggleDropdown = function ($event) {
            $event.preventDefault();
            $event.stopPropagation();
            $scope.status.isopen = !$scope.status.isopen;
        };
    };
    var NotificationController = function ($scope, notifications) {
        $scope.hide = false;
        $scope.init = function () {
            notifications.showError({
                message: 'Please verify your email to complete the sign-up process.',
                action: '<a class="btn btn-xs btn-default" href="/resend">Re-send verification email</a>',
                show: false,
                hide: $scope.hide
            });
        };
    };
    var SidebarJobApplicationController = function ($scope) {
        $scope.isCollapsed = false;
    };
    var SidebarJobAdvertController = function ($scope) {
        $scope.isCollapsed = true;
    };
    var SidebarJobServiceController = function ($scope) {
        $scope.isCollapsed = true;
    };
    app.controller("NavBarController", NavBarController);
    app.controller("NotificationController", NotificationController);
    app.controller("SidebarJobApplicationController", SidebarJobApplicationController);
    app.controller("SidebarJobAdvertController", SidebarJobAdvertController);
    app.controller("SidebarJobServiceController", SidebarJobServiceController);

}());
