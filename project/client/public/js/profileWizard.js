// app.js
// create our angular app and inject ngAnimate and ui-router
// =============================================================================
angular.module('mainApp', ['ui.router',
                           'flow',
                           'ngAutocomplete',
                           'ngCookies',
                           'ui.bootstrap',
                           'directives.customvalidation.customValidationTypes'])

// constants

// configuring our routes
// =============================================================================

    .config(function($stateProvider, $urlRouterProvider, flowFactoryProvider) {
          flowFactoryProvider.defaults = {
            target: 'http://localhost:5000/api/v1/profile-wizard/upload',
            permanentErrors: [404, 500, 501],
            maxChunkRetries: 1,
            chunkRetryInterval: 5000,
            simultaneousUploads: 4,
            singleFile: true
          };

          flowFactoryProvider.on('catchAll', function (event) {
          });

        $stateProvider
            // route to show our basic form (/form)
            .state('form', {
                url: '/form',
                templateUrl: '/html/wizard/form.html',
                controller: 'formController'
            })

            // nested states
            // each of these sections will have their own view
            // url will be nested (/form/profile)
            .state('form.profile', {
                url: '/profile',
                templateUrl: '/html/wizard/form-profile.html'
            })

            // url will be /form/interests
            .state('form.accountDetails', {
                url: '/account-details',
                templateUrl: '/html/wizard/form-accountDetails.html'
            })

            // url will be /form/payment
            .state('form.thanks', {
                url: '/thanks',
                templateUrl: '/html/wizard/form-thanks.html'
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
        templateUrl:'/html/wizard/autocomplete-template.html',
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
                scope.suggestions = filterFilter(scope.skills, scope.searchText);
            };

            $http.get('http://localhost:5000/api/v1/get_skills')
                .success(function (data) {
                    if (undefined !== data) {
                        skills_objects = data['skills'];
                        var skills = [];
                        skills_objects.forEach(function (element) {
                            skills.push(element.name);
                        });
                        scope.skills = skills;
                        scope.selectedIndex=-1;
                    }
                });

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
    
        
        // we will store all of our form data in this object
        $scope.formData = {};

        $scope.formData.result = '';
        $scope.formData.options = null;
        $scope.formData.details = '';
        $scope.formData.location = '';
        $scope.formData.photo = '';
        $scope.formData.skills = [];
        $scope.formData.gender = '';
        $scope.formData.current_job_status = '';


        // function to process the form
        $scope.processForm = function() {
            $http.post('http://localhost:5000/api/v1/create-profile',
                    {
                        address: $scope.formData.details.formatted_address,
                        token: $cookieStore.get('jp_token'),
                        gender: $scope.formData.gender,
                        skills: $scope.formData.skills,
                        current_job_status: $scope.formData.current_job_status
                    }).
                    success(function(data, status, headers, config) {
                        alert(data.token);
                    }).
                    error(function(data, status, headers, config) {
                        alert(status);

                    });
        };

        $http.get('http://localhost:5000/api/v1/get_ip').
          success(function(data, status, headers, config) {
            // this callback will be called asynchronously
            // when the response is available
            $scope.formData.location = data.location_info;
          }).
          error(function(data, status, headers, config) {
            // called asynchronously if an error occurs
            // or server returns response with an error status.
            console.log(status);
          });
    
        $scope.$watchCollection('formData.skills',function(val){
            console.log(val);
        });

    }).
    controller('addCookieCtrl', function($scope, $cookieStore){
        $scope.$on('flow::fileAdded', function (event, $flow, flowFile) {
            $flow.pause();
            $flow.opts.query.token = $cookieStore.get('jp_token');
            $cookieStore.put('image_uploaded','true');
            $flow.resume();
        });
      });

