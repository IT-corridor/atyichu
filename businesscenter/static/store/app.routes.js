angular.module('app.route', [
    'ngRoute',
    'common.controllers',
    'store.controllers',
])
.config(['$routeProvider','PATH',
    function($routeProvider, PATH) {
        $routeProvider.
        when('/', {
            templateUrl: PATH + 'common/templates/home.html',
            controller: 'CtrlHome',
        }).
        when('/stores/create/', {
            templateUrl: PATH + 'store/templates/create.html',
            controller: 'CtrlStoreCreate',
        }).
        when('/stores/my/', {
            templateUrl: PATH + 'store/templates/detail.html',
            controller: 'CtrlStoreOwn',
        }).
        when('/error/404/', {
            templateUrl: PATH + 'partials/error/404.html'}).
        otherwise({
            redirectTo: '/error/404/'
        });
    }
]);
