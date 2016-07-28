angular.module('app.route', [
    'ngRoute',
    'common.controllers',
    'store.controllers',
    'commodity.controllers',
    'photo.controllers',
    'group.controllers',
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
        when('/stores/my/edit', {
            templateUrl: PATH + 'store/templates/edit.html',
            controller: 'CtrlStoreEdit',
        }).
        when('/stores/my/commodities/', {
            templateUrl: PATH + 'commodity/templates/my_list.html',
            controller: 'CtrlMyCommodityList',
        }).
        when('/commodities/add', {
            templateUrl: PATH + 'commodity/templates/create.html',
            controller: 'CtrlCommodityCreate',
        }).
        when('/commodities/:pk/edit', {
            templateUrl: PATH + 'commodity/templates/update.html',
            controller: 'CtrlCommodityUpdate',
        }).
        when('/commodities/:pk', {
            templateUrl: PATH + 'commodity/templates/detail.html',
            controller: 'CtrlCommodityDetail',
        }).
        when('/commodities/', {
            templateUrl: PATH + 'commodity/templates/list.html',
            controller: 'CtrlCommodityList',
        }).
        when('/photo/newest', {
            templateUrl: PATH + 'group/templates/photo_list.html',
            controller: 'CtrlPhotoNewest',
            resolve: {
                title: function(){return 'Newest Photos';},
                kind: function(){return 'newest'},
            }
        }).
        when('/photo/liked', {
            templateUrl: PATH + 'group/templates/photo_list.html',
            controller: 'CtrlPhotoNewest',
            resolve: {
                title: function(){return 'Liked Photos';},
                kind: function(){return 'liked'},
            }
        }).
        when('/photo/:pk', {
            templateUrl: PATH + 'photo/templates/detail.html',
            controller: 'CtrlPhotoDetail'}).
        when('/photo/:pk/edit', {
            templateUrl: PATH + 'photo/templates/edit.html',
            controller: 'CtrlPhotoEdit'}).
        when('/photo/:pk/share', {
            templateUrl: PATH + 'photo/templates/clone.html',
            controller: 'CtrlPhotoClone'}).
        when('/error/404/', {
            templateUrl: PATH + 'partials/error/404.html'}).
        when('/group', {
            templateUrl: PATH + 'group/list.html',
            controller: 'CtrlGroupList',
            resolve: {
                title: function(){return 'Groups';},
                my: function(){return false},
            }
        }).
        when('/group/:pk/photo', {
            templateUrl: PATH + 'group/templates/photo_list.html',
            controller: 'CtrlGroupPhotoList'}).
        when('/group/:pk/photo/add', {
            templateUrl: PATH + 'group/templates/photo_add.html',
            controller: 'CtrlGroupPhotoAdd'}).
        when('/group/create', {
            templateUrl: PATH + 'group/templates/create.html',
            controller: 'CtrlGroupAdd'}).
        when('/group/:pk/manage', {
            templateUrl: PATH + 'group/templates/manage.html',
            controller: 'CtrlGroupManage'}).
        when('/my_groups', {
            templateUrl: PATH + 'group/templates/my.html',
            controller: 'CtrlGroupList',
            resolve: {
                title: function(){return 'My Groups';},
                my: function(){return true;},
            }
        }).
        otherwise({
            redirectTo: '/error/404/'
        });
    }
]);
