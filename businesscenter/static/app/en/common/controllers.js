angular.module('common.controllers', ['auth.services'])
.controller('CtrlDummy', ['$scope', '$rootScope','$http',
'$location', '$route', '$window', 'Auth','Signature',
    function($scope, $rootScope, $http, $location, $route, $window, Auth, Signature) {
        $rootScope.title = 'Dummy page';

        $rootScope.alerts.push({ type: 'info', msg: 'Welcome, stranger!' });

        $scope.loc = $window.location.href;


        $scope.logout = function(){
            Auth.remove();
            $route.reload();

        }
    }
]);