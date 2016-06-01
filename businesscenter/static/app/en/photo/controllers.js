angular.module('photo.controllers', [])
.controller('CtrlPhoto', ['$scope', '$rootScope', '$http',
'$location', 'Auth',
    function($scope, $rootScope, $http, $location, Auth) {
        $rootScope.title = 'Photo page';

        $rootScope.alerts.push({ type: 'info', msg: 'Welcome, stranger!' });
    }
]);