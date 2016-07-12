angular.module('common.controllers', ['auth.services', 'ngCookies'])
.controller('CtrlHome', ['$scope', '$rootScope','$http', '$cookies',
'$location', '$route', '$window', 'Auth', 'Logout',
    function($scope, $rootScope, $http, $cookies, $location, $route, $window, Auth, Logout) {

        $rootScope.title = 'The First Page';

    }
]);