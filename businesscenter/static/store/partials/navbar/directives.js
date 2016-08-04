var navbar = angular.module('navbar', ['auth.services'])
.directive('dNavbar', ['$window', '$location', '$routeParams', '$translate', 'PATH', 'Auth', '$uibModal',
                        function($window, $location, $routeParams, $translate, PATH, Auth, $uibModal) {
    return {
        restrict: 'A',
        templateUrl: PATH + 'partials/navbar/templates/navbar_d.html',
        controller: function($scope, $rootScope, $window, $location, $routeParams,
            $translate, PATH, Auth ){
            $rootScope.visitor_resolved = false;
            $scope.brand_text = 'ATYICHU';
            $scope.p = $routeParams;
            var auth_promise = Auth.is_authenticated();

            auth_promise.then(function(result){
                if (!result.is_authenticated){

                    $translate('AUTHENTICATION.REQUIRED').then(function (msg) {
                        $rootScope.alerts.push({ type: 'danger', msg:  msg});
                    });

                }
                else{
                    // Visitor means Vendor here!
                    // User instance logic migrated to the Auth factory
                    // This action should set $rootScope.visitor
                    Auth.get_user();
                }
            });

            $rootScope.$on("$routeChangeStart", function(event, next, current) {
                $scope.isCollapsed = false;
            });

            $scope.logout = function(){
                Auth.logout();
            }

            $scope.animationsEnabled = true;

            $scope.open = function () {

                var modalInstance = $uibModal.open({
                    animation: $scope.animationsEnabled,
                    templateUrl: PATH + 'partials/navbar/templates/modal.html',
                    controller: 'ModalInstanceCtrl',
                    size: 'sm',
                });

                modalInstance.result.then(function (auth) {
                    //$rootScope.alerts.push({ type: 'info', msg: 'Welcome, ' + auth.username + '!'});
                });
            }
            $scope.toggleAnimation = function () {
                $scope.animationsEnabled = !$scope.animationsEnabled;
            };

            $scope.search = function(keyEvent){
                //search
                if (keyEvent.which == 13){
                    $scope.search_c();
                }
            };

            $scope.search_c = function(){
                if ($scope.p.q){
                    $location.path('/photo/search').search({q: $scope.p.q});
                }
            };
        }
    };
}]);

navbar.controller('ModalInstanceCtrl', ['$scope','$rootScope', '$uibModalInstance' , 'Login', 'Auth',
                                        function ($scope, $rootScope, $uibModalInstance, Login, Auth) {

    $scope.authenticate = function(u, p){
        var promise = Auth.login(u, p);

        promise.then(
            function(success){
                $rootScope.visitor = success;
                $rootScope.visitor_resolved = true;
                $scope.error = null;
                Auth.set(success);
                $uibModalInstance.close(Auth);
            },
            function(error){
                $scope.error = error.data.error;
            }
        );
    }
    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    }
}]);