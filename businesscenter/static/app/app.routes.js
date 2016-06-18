angular.module('app.route', [
    'ngRoute',
    'common.controllers',
    'mirror.controllers',
    'photo.controllers',
    'user.controllers',
    'group.controllers',
])
.config(['$routeProvider','PATH',
    function($routeProvider, PATH) {
        $routeProvider.
        when('/', {
            templateUrl: PATH + 'common/common.html',
            controller: 'CtrlDummy'}).
        when('/mirror/', {
            templateUrl: PATH + 'mirror/list.html',
            controller: 'CtrlMirrorList'}).
        when('/mirror/:pk', {
            templateUrl: PATH + 'mirror/detail.html',
            controller: 'CtrlMirrorDetail'}).
        when('/photo/', {
            templateUrl: PATH + 'photo/list.html',
            controller: 'CtrlPhotoList'}).
        when('/photo/:pk', {
            templateUrl: PATH + 'photo/detail.html',
            controller: 'CtrlPhotoDetail'}).
        when('/photo/edit/:pk', {
            templateUrl: PATH + 'photo/edit.html',
            controller: 'CtrlPhotoEdit'}).
        when('/profile', {
            templateUrl: PATH + 'user/user.html',
            controller: 'CtrlProfile'}).
        when('/group/create', {
            templateUrl: PATH + 'group/group_create.html',
            controller: 'CtrlGroupAdd'}).
        when('/error/404/', {
            templateUrl: PATH + 'partials/error/404.html'}).
        otherwise({
            redirectTo: '/error/404/'
        });
    }
]);
