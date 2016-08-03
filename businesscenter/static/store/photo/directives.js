angular.module('photo.directives', ['commodity.services'])
.directive('commodityChoice', ['PATH', 'Commodity', function(PATH, Commodity) {
return {
  restrict: 'E',
  replace: true,
  templateUrl: PATH + 'photo/templates/commodity_dropdown.html',
  scope: {member:'=', placeholder:'=', commodities: '=', lim: '=', photo: '='},
  controller: function($scope, PATH, Commodity){

        $scope.active = 0;
        $scope.results = [];
        $scope.is_visible = false;
        $scope.set_active = function (index) {$scope.active = index;};

        $scope.get_results = function (text) {
            if (text !== ''){
                $scope.results = Commodity.my({q: text, photo: $scope.photo});
            }
        };

        $scope.input_blur = function(){
            if($scope.city){ $scope.results.length = 0 }
            $scope.is_visible = false;
        };
        $scope.select_item = function (index) {
            if ($scope.results.length > 0) {
                if ($scope.lim > $scope.commodities.length){
                    $scope.commodities.push($scope.results[index]);
                    $scope.commodity = '';
                    $scope.results.length = 0;

                }
            }
        };
    }
}
}]);