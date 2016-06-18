angular.module('group.controllers', ['auth.services', 'group.services'])
.controller('CtrlGroupAdd', ['$scope', '$rootScope','$http',
'$location', '$route', 'Auth', 'MultipartForm',
    function($scope, $rootScope, $http, $location, $route, Auth, MultipartForm) {

        $rootScope.title = 'New group';

        var auth_promise = Auth.is_authenticated();

        auth_promise.then(function(result){
            if (!result.is_authenticated){
                $window.location.replace("/visitor/");
            }
        });

        $scope.add = function() {
            var url = '/api/v1/group/';
            MultipartForm('#group_form', url).then(function(response) {
                $rootScope.alerts.push({ type: 'success', msg: 'Your drone was successfully added!'});
                    $location.path('/');
                },
                function(error) {
                    for (var e in error.data){
                        $rootScope.alerts.push({ type: 'danger', msg: error.data[e]});
                    }
                    $scope.error = error.data;
                }
            );

        };


    }
]);