var footer = angular.module('footer', [])
.directive('dFooter', ['PATH', function(PATH) {
    return {
        restrict: 'A',
        templateUrl: PATH + 'partials/footer/footer.html',
    }
}

]);