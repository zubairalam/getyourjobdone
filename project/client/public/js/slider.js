(function () {
    var app = angular.module('mainApp', ['ngAnimate', 'bzSlider']);
    var SliderController = function ($scope) {
        $scope.delay = 7000;
        $scope.slides = [
            {
                'title': 'hell',
                'class': 'animation-fade',
                'image': 'http://thumb9.shutterstock.com/display_pic_with_logo/722080/108056312/stock-photo-a-portrait-of-a-young-indian-business-woman-at-the-office-108056312.jpg'
            },
            {
                'title': 'sadas',
                'class': 'animation-fade',
                'image': 'http://thumb7.shutterstock.com/display_pic_with_logo/270058/111463571/stock-photo-beautiful-young-indian-white-collar-worker-opening-office-door-111463571.jpg'
            },
             {
                'title': 'heaven',
                'class': 'animation-fade',
                'image': 'http://thumb9.shutterstock.com/display_pic_with_logo/1002023/225762442/stock-photo-successful-business-woman-working-at-the-office-225762442.jpg'
            },
                         {
                'title': 'more',
                'class': 'animation-fade',
                'image': 'http://thumb9.shutterstock.com/display_pic_with_logo/270058/145004542/stock-photo-cheerful-young-indian-businessman-working-on-tablet-computer-in-office-145004542.jpg'
            }
        ];
    };
    app.controller("SliderController", SliderController);

}());


