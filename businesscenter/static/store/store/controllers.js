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
]);