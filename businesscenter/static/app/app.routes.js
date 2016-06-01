angular.module('app.route', [
    'ngRoute',
    'common.controllers',
    'mirror.controllers',
    'photo.controllers',
])
.config(['$routeProvider','PATH',
    function($routeProvider, PATH) {
        $routeProvider.
        when('/', {
            templateUrl: PATH + 'common/common.html',
            controller: 'CtrlDummy'}).
        when('/mirror/', {
            templateUrl: PATH + 'mirror/mirror.html',
            controller: 'CtrlMirror'}).
        when('/photo/', {
            templateUrl: PATH + 'photo/photo.html',
            controller: 'CtrlPhoto'}).
        when('/error/404/', {
            templateUrl: PATH + 'partials/error/404.html'}).
        otherwise({
            redirectTo: '/error/404/'
        });
    }
]);
