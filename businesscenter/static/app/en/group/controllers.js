angular.module('group.controllers', ['auth.services'])
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


    }
]);