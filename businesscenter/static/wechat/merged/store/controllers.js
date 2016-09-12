angular.module('store.controllers', ['store.services', 'common.services',])
    .controller('CtrlCommodityDetail', ['$scope', '$rootScope', '$http',
        '$location', '$routeParams', '$translate', 'Commodity',
        function ($scope, $rootScope, $http, $location, $routeParams, $translate,
                  Commodity) {
            $scope.commodity = Commodity.verbose({pk: $routeParams.pk});
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
    ]);
