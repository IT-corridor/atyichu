var navbar = angular.module('navbar', ['auth.services'])
.directive('dNavbar', ['Logout', 'Auth', '$window', 'PATH',
                        function(Logout, Auth, $window, PATH) {
    return {
        restrict: 'A',
        templateUrl: PATH + 'partials/navbar/navbar.html',
        controller: function($scope, $rootScope, Logout, Auth, $window, PATH){

            angular.element($window).bind('scroll', function() {
                $scope.change_class = (this.pageYOffset >= 100) ? true : false;
                $scope.$apply();
            });
            $scope.brand_text = 'ATYICHU';

            $scope.auth = Auth;

            if (!Auth.is_authenticated()){
                $window.location.replace("/visitor/?url=2");
            }
            $scope.logout = function(){
                $scope.r = Logout.query(function(r){
                    $rootScope.alerts.push({ type: 'info', msg: 'Good by.'});
                    $scope.auth.remove();
                });
            }

            $scope.animationsEnabled = true;
            $scope.toggleAnimation = function () {
                $scope.animationsEnabled = !$scope.animationsEnabled;
            };
        }
    };
}]);