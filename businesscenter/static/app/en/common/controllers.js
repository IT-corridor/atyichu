angular.module('common.controllers', ['auth.services'])
.controller('CtrlDummy', ['$scope', '$rootScope','$http',
'$location', '$route','Auth',
    function($scope, $rootScope, $http, $location, $route, Auth) {
        $rootScope.title = 'Dummy page';

        $rootScope.alerts.push({ type: 'info', msg: 'Welcome, stranger!' });

        $scope.logout = function(){
            Auth.remove();
            $route.reload();

        }
    }
]);