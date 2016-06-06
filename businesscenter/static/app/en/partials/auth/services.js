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

auth.factory('IsAuthenticated', ['$resource',
    function($resource){
        return $resource('visitor/is_authenticated/', {}, {
            get: {method:'GET', responseType:'json'},
        });
    }
]);
auth.factory('Auth', ['$cookies', 'IsAuthenticated',
function($cookies, IsAuthenticated){
    var auth = {};
    auth.get = function(key){
        return $cookies.get(key) ? $cookies.get(key) : null;
    };
    auth.set = function(username){
        $cookies.put('weixin', username);
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
        var response;
        IsAuthenticated.get(
            function(success){ response = true;}
            function(error){ response = false;}
        );
        //return this.username !== null;
    };
    return response;
}]);


auth.factory('Signature', ['$resource',
    function($resource){
        return $resource('snapshot/signature', {}, {
            get: {method:'GET', responseType:'json'},
        });
    }
]);