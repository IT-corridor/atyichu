angular.module('store.controllers', ['store.services', 'common.services',])
    .controller('CtrlCommodityDetail', ['$scope', '$rootScope', '$http',
        '$location', '$routeParams', '$translate', 'Commodity', '$uibModal', 'PATH',
        function ($scope, $rootScope, $http, $location, $routeParams, $translate,
                  Commodity, $uibModal, PATH) {
            $scope.commodity = Commodity.verbose({pk: $routeParams.pk});
            $scope.open_modal = function (resource) {
                var modalInstance = $uibModal.open({
                    animation: $scope.animationsEnabled,
                    templateUrl: PATH + 'store/templates/modal_' + resource + '.html',
                    controller: 'StoreModalInstanceCtrl',
                    size: 'md',
                    resolve: {
                        commodity: function () {
                            return $scope.commodity;
                        },
                        name: function () {
                            return resource;
                        }
                    }
                });

                modalInstance.result.then(
                    function (success) {
                        $translate('SUCCESS').then(function (msg) {
                            $rootScope.alerts.push({type: 'info', msg: msg});
                        });
                    }
                );
            };
        }
    ])
    .controller('CtrlStoreDetail', ['$scope', '$rootScope', '$http',
        '$location', '$translate', '$uibModal', '$log', 'PATH', 'Store', '$routeParams',
        function ($scope, $rootScope, $http, $location, $translate, $uibModal, $log, PATH,
                  Store, $routeParams) {

            $scope.r = Store.query({pk: $routeParams.pk});

            $scope.event_type = function (type) {
                if (type == 'promotion')
                    return 'b-info';
                else if (type == 'article')
                    return 'b-success';
                else
                    return 'b-primary';
            }

            $scope.toggleAnimation = function () {
                $scope.animationsEnabled = !$scope.animationsEnabled;
            };

        }
    ])
    .controller('StoreModalInstanceCtrl',
        ['$scope', '$uibModalInstance', 'name', 'commodity', '$translate', '$route', 'Commodity', '$location',
            function ($scope, $uibModalInstance, name, commodity, $translate, $route, Commodity, $location) {
                $scope.dict_data = {name: name};
                $scope.commodity = commodity;

                $scope.nearby_stores = Commodity.nearby_stores({pk: $scope.commodity.id});

                $scope.store_profile = function (id) {
                    $location.path('/store/' + id);
                    $uibModalInstance.dismiss('cancel');
                }
                $scope.cancel = function () {
                    $uibModalInstance.dismiss('cancel');
                }
            }
        ]);
