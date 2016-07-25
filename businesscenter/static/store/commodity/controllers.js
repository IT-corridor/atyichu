angular.module('commodity.controllers', ['commodity.services', 'common.services'])
.controller('CtrlCommodityCreate', ['$scope', '$rootScope','$http',
'$location', '$translate', 'MultipartForm', 'Store', 'Category', 'Kind', 'Size', 'Color',
    function($scope, $rootScope, $http, $location, $translate, MultipartForm,
    Store, Category, Kind, Size, Color) {

        $scope.wait = false;

        $scope.category_list = Category.query();
        $scope.brand_list = Store.my_brands();
        $scope.size_list = Size.query();
        $scope.color_list = Color.query();
        $scope.year = 2016;


        $scope.get_kind_list = function(){
            $scope.kind_list = Kind.query({category: $scope.category.id});
        }

        $translate(['COMMODITY.SEASONS.WINTER',
                    'COMMODITY.SEASONS.SPRING',
                    'COMMODITY.SEASONS.SUMMER',
                    'COMMODITY.SEASONS.AUTUMN',
                    ])
        .then(function (translations) {
            $scope.season_list = [{id: 0, title: translations['COMMODITY.SEASONS.WINTER']},
                                  {id: 1, title: translations['COMMODITY.SEASONS.SPRING']},
                                  {id: 2, title: translations['COMMODITY.SEASONS.SUMMER']},
                                  {id: 3, title: translations['COMMODITY.SEASONS.AUTUMN']}
            ];
        });

        $scope.create = function() {
            $scope.wait = true;
            var url = '/catalog/commodities/';
            MultipartForm('POST', '#commodity_form', url).then(function(response) {
                    $translate('COMMODITY.CREATE.SUCCESS').then(function (msg) {
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
]);
