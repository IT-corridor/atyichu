angular.module('common.controllers', ['auth.services'])
.controller('CtrlDummy', ['$scope', '$rootScope','$http',
'$location', '$route', '$window', 'Auth','Signature',
    function($scope, $rootScope, $http, $location, $route, $window, Auth, Signature) {
        $rootScope.title = 'Dummy page';

        $rootScope.alerts.push({ type: 'info', msg: 'Welcome, stranger!' });

        $scope.loc = $window.location.href;
        /*$scope.js_info = Signature.get({location: $scope.loc}, function (success){
            wx.config({
                debug: false,
                appId: success.appId,
                timestamp: success.timestamp,
                nonceStr: success.noncestr,
                signature: success.signature,
                jsApiList: ['getLocation']
            });
            wx.ready(function () {

                wx.getLocation({
                    success: function (res) {
                        alert("get location!");
                        $scope.lat = res.latitude;
                        $scope.lon = res.longitude;
                        console.log(res);

                    },
                    cancel: function (res) {
                        alert('Cancel');
                    }
                });
                $scope.$apply();
            });
            wx.error(function(res){

                $scope.error = res;
                $scope.apply();
            });
        });*/

        $scope.logout = function(){
            Auth.remove();
            $route.reload();

        }
    }
]);