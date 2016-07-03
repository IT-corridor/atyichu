var app = angular.module('app.main', [
    'ngAnimate',
    'ngAria',
    'ngTouch',
    'ui.bootstrap',
    'constants',
    'app.route',
    'auth.services',
    'weixinapi',
    'navbar',
    'footer',
    'alert',
    'selfie',
]);
app.factory('httpRequestInterceptor', function () {
    return {
        request: function (config) {
            config.headers['X-Requested-With'] = 'XMLHttpRequest';
            return config;
        }
    };
});
app.run(function($rootScope) {
    //$rootScope.site = 'atyichu.cn';
    $rootScope.site = '哎特衣橱';
    $rootScope.THEME = '/static/theme/';
});
app.config(function ($httpProvider) {
    $httpProvider.interceptors.push('httpRequestInterceptor');
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.useApplyAsync(true);
});
app.config(function($resourceProvider) {
  $resourceProvider.defaults.stripTrailingSlashes = false;
});
app.config(['$locationProvider', function($locationProvider){
    //$locationProvider.html5Mode(true);
    $locationProvider.hashPrefix('!');
}]);