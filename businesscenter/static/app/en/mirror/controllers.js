angular.module('mirror.controllers', [])
.controller('CtrlMirror', ['$scope', '$rootScope', '$http',
'$location', 'Auth',
    function($scope, $rootScope, $http, $location, Auth) {
        $rootScope.title = 'Mirror page';
        $rootScope.alerts.push({ type: 'info', msg: 'Welcome, stranger!' });
    }
]);
