angular.module('store.controllers', ['store.services', 'common.services',])
.controller('CtrlCommodityDetail', ['$scope', '$rootScope','$http',
'$location', '$routeParams', '$translate', 'Commodity',
    function($scope, $rootScope, $http, $location, $routeParams, $translate,
    Commodity) {
        $scope.commodity = Commodity.verbose({pk: $routeParams.pk});
    }
])

