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
            templateUrl: PATH + 'group/photo_list.html',
            controller: 'CtrlPhotoNewest',
            resolve: {
                title: function(){return 'Newest Photos';},
                kind: function(){return 'newest'},
            }
        }).
        when('/mirror/', {
            templateUrl: PATH + 'mirror/list.html',
            controller: 'CtrlMirrorList'}).
        when('/mirror/:pk', {
            templateUrl: PATH + 'mirror/detail.html',
            controller: 'CtrlMirrorDetail'}).
        when('/photo/newest', {
            templateUrl: PATH + 'group/photo_list.html',
            controller: 'CtrlPhotoNewest',
            resolve: {
                title: function(){return 'Newest Photos';},
                kind: function(){return 'newest'},
            }
        }).
        when('/photo/liked', {
            templateUrl: PATH + 'group/photo_list.html',
            controller: 'CtrlPhotoNewest',
            resolve: {
                title: function(){return 'Liked Photos';},
                kind: function(){return 'liked'},
            }
        }).
        when('/photo/:pk', {
            templateUrl: PATH + 'photo/detail.html',
            controller: 'CtrlPhotoDetail'}).
        when('/photo/:pk/edit', {
            templateUrl: PATH + 'photo/edit.html',
            controller: 'CtrlPhotoEdit'}).
        when('/photo/:pk/share', {
            templateUrl: PATH + 'photo/clone.html',
            controller: 'CtrlPhotoClone'}).
        when('/profile', {
            templateUrl: PATH + 'user/user.html',
            controller: 'CtrlProfile'}).
        when('/group', {
            templateUrl: PATH + 'group/list.html',
            controller: 'CtrlGroupList',
            resolve: {
                title: function(){return 'Groups';},
                my: function(){return false},
            }
        }).
        when('/group/:pk/photo', {
            templateUrl: PATH + 'group/photo_list.html',
            controller: 'CtrlGroupPhotoList'}).
        when('/group/:pk/photo/add', {
            templateUrl: PATH + 'group/photo_add.html',
            controller: 'CtrlGroupPhotoAdd'}).
        when('/group/create', {
            templateUrl: PATH + 'group/create.html',
            controller: 'CtrlGroupAdd'}).
        when('/group/:pk/manage', {
            templateUrl: PATH + 'group/manage.html',
            controller: 'CtrlGroupManage'}).
        when('/my_groups', {
            templateUrl: PATH + 'group/my.html',
            controller: 'CtrlGroupList',
            resolve: {
                title: function(){return 'My Groups';},
                my: function(){return true;},
            }
        }).
        when('/error/404/', {
            templateUrl: PATH + 'partials/error/404.html'}).
        otherwise({
            redirectTo: '/error/404/'
        });
    }
]);
