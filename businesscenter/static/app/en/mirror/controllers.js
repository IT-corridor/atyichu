angular.module('mirror.controllers', ['mirror.services'])
.controller('CtrlMirror', ['$scope', '$rootScope', '$http',
'$location', 'Auth', 'Mirror',
    function($scope, $rootScope, $http, $location, Auth, Mirror) {
        $rootScope.title = 'Mirror page';
        $rootScope.alerts.push({ type: 'info', msg: 'You  view mirror list!' });
        $scope.mirrors = Mirror.query();
    }
]);
