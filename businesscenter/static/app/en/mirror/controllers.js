angular.module('mirror.controllers', ['mirror.services'])
.controller('CtrlMirror', ['$scope', '$rootScope', '$http',
'$location', 'Auth', 'Mirror', 'WXI',
    function($scope, $rootScope, $http, $location, Auth, Mirror, WXI) {
        $rootScope.title = 'Mirror page';
        $rootScope.alerts.push({ type: 'info', msg: 'You  view mirror list!' });

        var promise = WXI.get_location();

        promise.then(function(result){
            $scope.mirrors = Mirror.query(result,
                function(success){
                    $scope.status = 'OK';
                },
                function(error){
                    $scope.status = error.data;
                }
            );
        });


    }
]);
