angular.module('commodity.directives', ['commodity.services'])
    .directive('stockSet', ['PATH', 'Color', 'Size',
        function(PATH) {
            return {
                restrict: 'AC',
                scope: {
                    stockstr: '=',
                },
                templateUrl: PATH + 'commodity/templates/include/stock_set.html',
                controller: function($scope, Color, Size) {
                    $scope.size_list = Size.query();
                    $scope.color_list = Color.query();
                    $scope.placeholder_list = [{
                        color: null,
                        size: null,
                        amount: 0
                    }];

                    $scope.refresh_stock_set = function() {
                        var data = $scope.placeholder_list.slice(),
                            len = data.length,
                            i = 0;
                        for (i; i < len; i++) {
                            if (data[i]['size'] == null) {
                                console.log('splice');
                                data.splice(i, 1);
                            }
                        }
                        $scope.stockstr = angular.toJson(data);

                    };

                    $scope.add_stock = function() {
                        $scope.placeholder_list.push({
                            color: null,
                            size: null,
                            amount: 0
                        });
                    };
                }
            }
        }

    ]);
