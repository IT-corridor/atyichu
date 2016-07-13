angular.module('store.controllers', ['store.services','common.services', 'auth.services'])
.controller('CtrlStoreCreate', ['$scope', '$rootScope','$http',
'$location', '$translate', 'MultipartForm',
    function($scope, $rootScope, $http, $location, $translate, MultipartForm) {

        $scope.wait = false;

        $scope.create = function() {
            $scope.wait = true;
            var url = '/account/stores/';
            MultipartForm('POST', '#store_form', url).then(function(response) {
                    $translate('STORE.CREATE.SUCCESS').then(function (msg) {
                        $rootScope.alerts.push({ type: 'info', msg:  msg});
                    });
                    $rootScope.visitor.store = response.data.id;
                    $location.path('/stores/my/');


                },
                function(error) {
                    $scope.error = error.data;
                    $scope.wait = false;
                }
            );

        };

    }
])
.controller('CtrlStoreOwn', ['$scope', '$rootScope','$http',
'$location', '$translate', 'Store',
    function($scope, $rootScope, $http, $location, $translate, Store) {

        $scope.r = Store.my_store();

    }
])
.controller('CtrlStoreEdit', ['$scope', '$rootScope', '$http',
    '$window', '$location', '$translate', 'Store', 'MultipartForm',
    function($scope, $rootScope, $http, $window, $location, $translate, Store, MultipartForm) {

        $scope.wait = false;

        function handle_error(error){
            $translate('STORE.UPDATE.FAIL').then(function (msg) {
                $rootScope.alerts.push({ type: 'danger', msg:  msg});
                $scope.wait = false;
                console.log(error.data);
            });
        }

        $scope.r = Store.my_store(
            function(success){},
            handle_error
        );

        $scope.update = function(){
            $scope.wait = true;
            var data = $scope.r;
            delete data['photo'];
            delete data['thumb'];
            Store.update({pk: $scope.r.id}, data,
                function(success){
                    $translate('STORE.UPDATE.SUCCESS').then(function (msg) {
                        $rootScope.alerts.push({ type: 'info', msg:  msg});
                    });
                    $location.path('/stores/my/');
                },
                handle_error
            );
        };

        $scope.update_photo = function() {
            $scope.wait = true;
            var url = '/account/stores/'+ $scope.r.id + '/update_photo/';
            MultipartForm('PATCH', '#photo_form', url).then(function(response) {
                    $translate('STORE.UPDATE.SUCCESS').then(function (msg) {
                        $rootScope.alerts.push({ type: 'info', msg:  msg});
                    });
                    $location.path('/stores/my/');
                },
                function(error) {
                    $scope.error = error.data;
                    $scope.wait = false;
                }
            );

        };
    }
]);