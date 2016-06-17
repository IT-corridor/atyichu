var navbar = angular.module('navbar', ['auth.services', 'selfie'])
.directive('dNavbar', ['$window', 'PATH','Logout', 'Auth', 'Update', 'Me',
                        function($window, PATH, Logout, Auth, Update, Me) {
    return {
        restrict: 'A',
        templateUrl: PATH + 'partials/navbar/navbar.html',
        controller: function($scope, $rootScope, $window, PATH, Logout, Auth, Update, Me ){

            angular.element($window).bind('scroll', function() {
                $scope.change_class = (this.pageYOffset >= 100) ? true : false;
                $scope.$apply();
            });
            $scope.brand_text = 'ATYICHU';

            $scope.auth = Auth;

            var auth_promise = Auth.is_authenticated();

            auth_promise.then(function(result){
                if (!result.is_authenticated){
                    //$window.location.replace("/visitor/");
                }
                else{
                    // Maybe need to optimize...
                    $scope.visitor = Me.get();
                }
            });


            $scope.logout = function(){
                $scope.r = Logout.query(function(r){
                    $rootScope.alerts.push({ type: 'info', msg: 'Good by.'});
                    $scope.auth.remove();
                });
            }

            $scope.sync_profile = function(){

                Update.post(function(success){
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
            $scope.animationsEnabled = true;
            $scope.toggleAnimation = function () {
                $scope.animationsEnabled = !$scope.animationsEnabled;
            };
        }
    };
}]);