angular.module('common.controllers', [])
.controller('CtrlDummy', ['$scope', '$rootScope', '$http',
'$location', 'Auth',
    function($scope, $rootScope, $http, $location, Auth) {
        $rootScope.title = 'Dummy page';


        $rootScope.alerts.push({ type: 'info', msg: 'Welcome, stranger!' });
        if (Auth.is_authenticated()){
            $location.path('/');
        }
    }
]);