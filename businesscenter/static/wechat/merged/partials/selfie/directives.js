angular.module('selfie', ['auth.services'])
.directive('wxSelf', ['PATH', function(PATH) {
    return {
        restrict: 'E',
        replace: true,
        transclude: true,
        templateUrl: PATH + 'partials/selfie/templates/block.html',
        scope: {visitor:'='}
    }
}]);
