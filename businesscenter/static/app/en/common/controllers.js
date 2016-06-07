angular.module('common.controllers', ['auth.services'])
.controller('CtrlDummy', ['$scope', '$rootScope','$http',
'$location', '$route', '$window', 'Auth', 'Logout', 'WXI',
    function($scope, $rootScope, $http, $location, $route, $window, Auth, Logout, WXI) {

        $rootScope.title = 'Dummy page';

        $rootScope.alerts.push({ type: 'info', msg: 'Welcome, stranger!' });

        var promise = WXI.get_location();
        promise.then(function(success){
            $scope.lat = success.latitude;
            $scope.lon = success.longitude;
        });

        $scope.logout = function(){
            $scope.r = Logout.query(function(r){
                $rootScope.alerts.push({ type: 'info', msg: 'Good by.'});
                $route.reload();
                //$scope.auth.remove();
            });
        };
    }
]);