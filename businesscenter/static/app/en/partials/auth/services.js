var auth = angular.module('auth.services', ['ngResource', 'ngCookies']);

auth.factory('Login', ['$resource',
    function($resource){
        return $resource('visitor/', {}, {
            query: {method:'GET', responseType:'json'},
        });
    }
]);
auth.factory('Update', ['$resource',
    function($resource){
        return $resource('visitor/update/', {}, {
            post: {method:'POST', responseType:'json'},
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
auth.factory('Me', ['$resource',
    function($resource){
        return $resource('visitor/me/', {}, {
            get: {method:'GET', responseType:'json'},
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

        return IsAuthenticated.get().$promise;
        //return this.username !== null;
    };
    return auth;
}]);
