angular.module('store.controllers', ['store.services', 'common.services',])
.controller('CtrlCommodityDetail', ['$scope', '$rootScope','$http', '$window',
'$location', '$routeParams', '$translate', 'Commodity',
    function($scope, $rootScope, $http, $window, $location, $routeParams, $translate,
    Commodity) {

        var body = document.body,
            html = document.documentElement;

        $scope.height = Math.max(body.scrollHeight, body.offsetHeight,
        html.clientHeight, html.scrollHeight, html.offsetHeight );

        $scope.width = Math.max(body.scrollWidth, body.offsetWidth,
        html.clientWidth, html.scrollWidth, html.offsetWidth );

        console.log($scope.width);
        console.log($scope.height);

        $scope.carousel = {index:0};
        $scope.commodity = Commodity.verbose({pk: $routeParams.pk},
            function(success){
                $scope.slides = success.gallery_set;
            }
        );
        $scope.prev_slide = function(){
            if ($scope.carousel.index > 1){
                $scope.carousel.index -= 1;
                console.log($scope.carousel.index);
            }

        };
        $scope.next_slide = function(){

            if ($scope.carousel.index < $scope.slides.length - 1 ){
                $scope.carousel.index += 1;
                console.log($scope.carousel.index);
            }

        };
        $scope.set_index = function(index){
            $scope.carousel.index = index;
            console.log($scope.carousel.index);
        };
    }
]);

