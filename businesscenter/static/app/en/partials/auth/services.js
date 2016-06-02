var auth = angular.module('auth.services', ['ngResource', 'ngCookies']);

auth.factory('Login', ['$resource',
    function($resource){
        return $resource('visitor/', {}, {
            query: {method:'GET', responseType:'json'},
        });
    }
]);

auth.factory('Logout', ['$resource',
    function($resource){
        return $resource('visitor/logout/', {}, {
            query: {method:'GET', responseType:'json'},
        });
    }
]);

auth.factory('Auth', ['$cookies', function($cookies){
    var auth = {};
    auth.get = function(key){
        return $cookies.getObject(key) ? $cookies.getObject(key) : null;
    };
    auth.set = function(username){
        $cookies.putObject('weixin', username);
        this.refresh();
    };
    auth.refresh = function(){
        this.username = this.get('weixin');
    };
    auth.remove = function(){
        $cookies.remove('weixin');
        this.refresh();
    };
    auth.username = auth.get('weixin');
    auth.is_authenticated = function(){
        this.username !== null;
    };
    return auth;
}]);

