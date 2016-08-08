angular.module('user.controllers', ['auth.services'])
.controller('CtrlProfile', ['$scope', '$rootScope','$http',
'$location', '$route', 'Auth', 'Logout', 'Me', 'ProfileSync',
    function($scope, $rootScope, $http, $location, $route, Auth, Logout, Me, ProfileSync) {

        $rootScope.title = 'My profile';

        $scope.me = $rootScope.visitor;


        $scope.logout = function(){
            $scope.r = Logout.query(function(success){
                Auth.remove();
                $rootScope.alerts.push({ type: 'info', msg: 'Good by.'});
                //$route.reload();
                  $location.path('/');
            });
        };

        $scope.sync_profile = function(){

            ProfileSync.post(function(success){
                $rootScope.visitor = success;
                $rootScope.alerts.push({ type: 'info',
                    msg: 'Profile was updated.'});
                $location.path('/');
                },
                function(error){
                    for (var e in error.data){
                        $rootScope.alerts.push({ type: 'danger', msg: error.data[e]});
                    }
                    $location.path('/');
                }

            );

        }
    }
]);