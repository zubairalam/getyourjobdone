// app.js
// create our angular app and inject ngAnimate and ui-router
// =============================================================================
angular.module('mainApp', ['ui.router',
                            'flow',
                            'ngCookies',
                            'ngAutocomplete',
                            'ui.bootstrap',
                            'directives.customvalidation.customValidationTypes',
                            'ngTagsInput'])

// constants

// configuring our routes
// =============================================================================

    .config(function ($stateProvider, $urlRouterProvider, flowFactoryProvider) {
          flowFactoryProvider.defaults = {
            target: 'http://localhost:5000/api/v1/profile-wizard/upload',
            permanentErrors: [404, 500, 501],
            maxChunkRetries: 1,
            chunkRetryInterval: 5000,
            simultaneousUploads: 4,
            singleFile: true
          };

          flowFactoryProvider.on('catchAll', function (event) {
            console.log('catchAll', arguments);
          });

        $stateProvider
            // route to show our basic form (/form)
            .state('form', {
                url: '/form',
                templateUrl: '/html/cp-wizard/form.html',
                controller: 'formController'
            })

            // nested states
            // each of these sections will have their own view
            // url will be nested (/form/profile)
            .state('form.profile', {
                url: '/profile',
                templateUrl: '/html/cp-wizard/form-profile.html'
            })

            // url will be /form/interests
            .state('form.accountDetails', {
                url: '/account-details',
                templateUrl: '/html/cp-wizard/form-accountDetails.html'
            })

            // url will be /form/payment
            .state('form.thanks', {
                url: '/thanks',
                templateUrl: '/html/cp-wizard/form-thanks.html'
            });

        // catch all route
        // send users to the form page
        $urlRouterProvider.otherwise('/form/profile');
    })

.directive('autoComplete',['$http', 'filterFilter',function($http, filterFilter){
    return {
        restrict:'AE',
        scope:{
            selectedTags:'=model'
        },
        templateUrl:'/html/cp-wizard/autocomplete-template.html',
        link:function(scope,elem,attrs){

            scope.suggestions=[];

            scope.selectedTags=[];

            scope.selectedIndex=-1;

            scope.removeTag=function(index){
                scope.selectedTags.splice(index,1);
            }

            /*scope.search=function(){
                $http.get(attrs.url+'?term='+scope.searchText).success(function(data){
                    if(data.indexOf(scope.searchText)===-1){
                        data.unshift(scope.searchText);
                    }
                    scope.suggestions=data;
                    scope.selectedIndex=-1;
                });
            }*/
            
            scope.search = function () {
                console.log("aya: ", scope.searchText);
                scope.suggestions = filterFilter(scope.skills, scope.searchText);
            };

            /*$http.get('http://localhost:5000/api/v1/get_skills')
                .success(function (data) {
                    if (undefined !== data) {
                        console.log(data);
                        skills_objects = data['skills'];
                        var skills = [];
                        skills_objects.forEach(function (element) {
                            skills.push(element.name);
                        });
                        scope.skills = skills;
                        scope.selectedIndex=-1;
                    }
                    //if (data.length > 0) {
                        //scope.suggestions = data;
                        //scope.selectedIndex=-1;
                    //}
                });*/

            scope.addToSelectedTags=function(index){
                if(scope.suggestions.length>0 && scope.selectedTags.indexOf(scope.suggestions[index])===-1){
                    scope.selectedTags.push(scope.suggestions[index]);
                    scope.searchText='';
                    scope.suggestions=[];
                } 
                else if (scope.suggestions.length===0) {
                    /* if not found in suggestions and user wants to add that to his skills list */
                    scope.selectedTags.push(scope.searchText);
                    scope.searchText='';
                }
            }

            scope.checkKeyDown=function(event){
                if(event.keyCode===40){
                    event.preventDefault();
                    if(scope.selectedIndex+1 !== scope.suggestions.length){
                        scope.selectedIndex++;
                    }
                }
                else if(event.keyCode===38){
                    event.preventDefault();
                    if(scope.selectedIndex-1 !== -1){
                        scope.selectedIndex--;
                    }
                }
                else if(event.keyCode===13){
                    event.preventDefault();
                    scope.addToSelectedTags(scope.selectedIndex);
                }
            }

            scope.$watch('selectedIndex',function(val){
                if(val!==-1) {
                    scope.searchText = scope.suggestions[scope.selectedIndex];
                }
            });
        }
    }
}])

// our controller for the form
// =============================================================================
    .controller('formController', function($http, $scope, $cookieStore) {

        
        var urlRegExp = /^(?:(?:https?|ftp):\/\/)(?:\S+(?::\S*)?@)?(?:(?!10(?:\.\d{1,3}){3})(?!127(?:\.\d{1,3}){3})(?!169\.254(?:\.\d{1,3}){2})(?!192\.168(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:\/[^\s]*)?$/i;

        angular.extend($scope, {
            urlValidator: [
                {
                    errorMessage: 'It must be a valid url (i.e. http://www.example.com)',
                    validator: function (errorMessageElement, val, attr, element, model, modelCtrl){
                        return urlRegExp.test(val);
                    }
                }
            ]
        });        
        

        // we will store all of our form data in this object
        $scope.formData = {};

        $scope.formData.details = '';
        $scope.formData.location = '';
        $scope.companyTypes = ['Private', 'Public', 'Charity', 'Government'];
        $scope.companySizes = ['Small', 'Medium', 'Large'];
        $scope.industries = [];
        $scope.formData.hiring = '';
        $scope.formData.companyType = '';
        $scope.formData.companySize = '';
        $scope.formData.name = '';
        $scope.formData.services = [];

        // function to process the form
        $scope.processForm = function() {
            $http.post('http://localhost:5000/api/v1/create-company-profile',
                    {
                        user_id: $cookieStore.get('jp_id'),
                        address: $scope.formData.details.formatted_address,
                        name: $scope.formData.name,
                        website: $scope.formData.website,
                        companyType: $scope.formData.companyType,
                        companySize: $scope.formData.companySize,
                        hiring: $scope.formData.hiring,
                        industry: $scope.formData.industry._id,
                        services: $scope.formData.services
                    }).
                    success(function(data, status, headers, config) {
                        alert(data.message);
                    }).
                    error(function(data, status, headers, config) {
                        alert(data.message);
                    });
        };

        $http.get('http://localhost:5000/api/v1/get_ip').
          success(function (data, status, headers, config) {
            // this callback will be called asynchronously
            // when the response is available
            $scope.formData.location = data.location_info;
          }).
          error(function (data, status, headers, config) {
            // called asynchronously if an error occurs
            // or server returns response with an error status.
            console.log(status);
          });
    
        $http.get('http://localhost:5000/api/v1/industries')
            .success(function (data, status, headers, config) {
                $scope.industries = data;
            })
            .error(function (data, status, headers, config) {});
    
        
    }).
    controller('addCookieCtrl', function($scope, $cookieStore){
        $scope.$on('flow::fileAdded', function (event, $flow, flowFile) {
            $flow.pause();
            $flow.opts.query.token = $cookieStore.get('jp_token');
            $cookieStore.put('image_uploaded','true');
            $flow.resume();
        });
      });

