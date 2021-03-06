angular.module('store.controllers', ['store.services', 'common.services', 'auth.services', 'commodity.services'])
    .controller('CtrlStoreCreate', ['$scope', '$rootScope', '$http',
        '$location', '$translate', 'MultipartForm',
        function ($scope, $rootScope, $http, $location, $translate, MultipartForm) {

            $scope.wait = false;

            $scope.create = function () {
                $scope.wait = true;
                var url = '/account/stores/';
                MultipartForm('POST', '#store_form', url).then(function (response) {
                        $translate('STORE.CREATE.SUCCESS').then(function (msg) {
                            $rootScope.alerts.push({type: 'info', msg: msg});
                        });
                        $rootScope.visitor.store = response.data.id;
                        $location.path('/stores/my/');


                    },
                    function (error) {
                        $scope.error = error.data;
                        $scope.wait = false;
                    }
                );

            };

        }
    ])
    .controller('CtrlStoreOwn', ['$scope', '$rootScope', '$http',
        '$location', '$translate', '$uibModal', '$log', 'PATH', 'Store', 'Brand', 'Promotion',
        function ($scope, $rootScope, $http, $location, $translate, $uibModal, $log, PATH,
                  Store, Brand, Promotion) {

            $scope.r = Store.my_store();

            $scope.resource_map = {
                'brand': Brand,
                'promotion': Promotion,
            };

            $scope.event_type = function (type) {
                if (type == 'promotion')
                    return 'b-info';
                else if (type == 'article')
                    return 'b-success';
                else
                    return 'b-primary';
            }
            $scope.open_modal = function (resource) {

                var modalInstance = $uibModal.open({
                    animation: $scope.animationsEnabled,
                    templateUrl: PATH + 'store/templates/modal_' + resource + '.html',
                    controller: 'StoreModalInstanceCtrl',
                    size: 'lg',
                    resolve: {
                        resource: function () {
                            return $scope.resource_map[resource];
                        },
                        name: function () {
                            return resource;
                        },
                        store: function () {
                            return $scope.r.vendor;
                        }
                    }
                });

                modalInstance.result.then(
                    function (success) {
                        $translate('SUCCESS').then(function (msg) {
                            $rootScope.alerts.push({type: 'info', msg: msg});
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
        function ($scope, $rootScope, $http, $window, $location, $translate, Store, MultipartForm) {

            $scope.wait = false;

            function handle_error(error) {
                $translate('STORE.UPDATE.FAIL').then(function (msg) {
                    $rootScope.alerts.push({type: 'danger', msg: msg});
                    $scope.wait = false;
                    console.log(error.data);
                });
            }

            $scope.r = Store.my_store(
                function (success) {
                },
                handle_error
            );

            $scope.update = function () {
                $scope.wait = true;
                var data = $scope.r;
                delete data['photo'];
                delete data['thumb'];
                delete data['crop'];
                delete data['post'];
                console.log($scope.r);
                Store.update({pk: $scope.r.vendor}, data,
                    function (success) {
                        $translate('STORE.UPDATE.SUCCESS').then(function (msg) {
                            // $rootScope.alerts.push({type: 'info', msg: msg});
                            // $rootScope.alerts.push({type: 'info', msg: 'Successfully updated!'});
                        });
                        $location.path('/stores/my/');
                    },
                    handle_error
                );
            };

            $scope.getLocation = function (val) {
                return $http.jsonp('http://apis.map.qq.com/ws/place/v1/suggestion', {
                    params: {
                        region: $scope.r.state_title,
                        keyword: val,
                        key: 'NY6BZ-2IB35-AMFIV-QMWBJ-RKC2Z-6BFDG',
                        output: 'jsonp',
                        callback: 'JSON_CALLBACK',
                    }
                }).then(function (response) {
                    return response.data.data.map(function (item) {
                        return item;
                    });
                });
            };

            $scope.get_item_ = function ($item, $model, $label, $event) {
                $scope.r.state_title = $item.province
                $scope.r.city_title = $item.city
                $scope.r.district_title = $item.district
                $scope.r.lat = $item.location.lat
                $scope.r.lng= $item.location.lng
            }

            $scope.update_photo = function () {
                $scope.wait = true;
                var url = '/account/stores/' + $scope.r.vendor + '/update_photo/';
                MultipartForm('PATCH', '#photo_form', url).then(function (response) {
                        $translate('STORE.UPDATE.SUCCESS').then(function (msg) {
                            $rootScope.alerts.push({type: 'info', msg: msg});
                        });
                        $location.path('/stores/my/');
                    },
                    function (error) {
                        $scope.error = error.data;
                        $scope.wait = false;
                    }
                );
            };

            $scope.update_post = function () {
                $scope.wait = true;
                var url = '/account/stores/' + $scope.r.vendor + '/update_post/';
                MultipartForm('PATCH', '#post_form', url).then(function (response) {
                        $translate('STORE.UPDATE.SUCCESS').then(function (msg) {
                            $rootScope.alerts.push({type: 'info', msg: msg});
                        });
                        $location.path('/stores/my/');
                    },
                    function (error) {
                        $scope.error = error.data;
                        $scope.wait = false;
                    }
                );
            };
        }
    ])
    .controller('StoreModalInstanceCtrl',
        ['$scope', '$rootScope', '$uibModalInstance', 'resource', 'name', 'MultipartForm', 'store', '$translate', '$route',
            function ($scope, $rootScope, $uibModalInstance, resource, name, MultipartForm, store, $translate, $route) {
                $scope.dict_data = {name: name};
                $scope.data = {};
                $scope.store = store;

                $scope.create = function () {
                    if (name == 'promotion') {
                        $scope.wait = true;
                        var url = '/catalog/promotions/';
                        MultipartForm('POST', '#promotion_form', url).then(function (response) {
                                $translate('STORE.UPDATE.SUCCESS').then(function (msg) {
                                    $rootScope.alerts.push({type: 'info', msg: msg});
                                });
                                $route.reload();
                                $uibModalInstance.close();
                            },
                            function (error) {
                                $scope.error = error.data;
                                $scope.wait = false;
                            }
                        );

                    } else {
                        resource.save($scope.data,
                            function (success) {
                                $uibModalInstance.close(success);
                            },
                            function (error) {
                                $scope.error = error.data;
                                console.log($scope.error);
                            }
                        );
                    }
                }
                $scope.cancel = function () {
                    $uibModalInstance.dismiss('cancel');
                }
            }
        ]);