angular.module('store.controllers', ['store.services','common.services', 'auth.services', 'commodity.services'])
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
'$location', '$translate', '$uibModal', '$log', 'PATH', 'Store', 'Brand',
    function($scope, $rootScope, $http, $location, $translate, $uibModal, $log, PATH,
    Store, Brand) {

        $scope.r = Store.my_store();

        $scope.resource_map = {
            'brand': Brand,
        };

        $scope.open_modal = function (resource) {

        var modalInstance = $uibModal.open({
            animation: $scope.animationsEnabled,
            templateUrl: PATH +'store/templates/modal_' + resource + '.html',
            controller: 'StoreModalInstanceCtrl',
            size: 'lg',
            resolve: {
                resource: function () {
                    return $scope.resource_map[resource];
                },
                name: function(){
                    return resource;
                },
            }
        });

    modalInstance.result.then(
        function (success) {
            $translate('SUCCESS').then(function (msg) {
                $rootScope.alerts.push({ type: 'info', msg:  msg});
            });
        },
        function () {
            $log.info('Modal dismissed at: ' + new Date());
        }
    );
  };

    $scope.toggleAnimation = function () {
        $scope.animationsEnabled = !$scope.animationsEnabled;
    };

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
            delete data['crop'];
            console.log($scope.r);
            Store.update({pk: $scope.r.vendor}, data,
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
])
.controller('StoreModalInstanceCtrl',
    ['$scope','$rootScope', '$uibModalInstance' , 'resource', 'name',
    function ($scope, $rootScope, $uibModalInstance, resource, name) {
        $scope.dict_data = {name: name};
        $scope.data = {};
        $scope.create = function(){
            resource.save($scope.data,
                function(success){
                    $uibModalInstance.close(success);
                },
                function(error){

                    $scope.error = error.data;
                    console.log($scope.error);
                }
            );
        }
        $scope.cancel = function () {
            $uibModalInstance.dismiss('cancel');
        }
    }
]);