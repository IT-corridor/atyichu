var auth = angular.module('auth.services', ['ngResource', 'ngCookies']);

auth.factory('Login', ['$resource',
    function($resource){
        return $resource('visitor/', {}, {
            query: {method:'GET', responseType:'json'},
        });
    }
]);
auth.factory('ProfileSync', ['$resource',
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
auth.factory('IsSmartDevice', ['$window',
    function($window){
        return function(){
            // Checks for iOs, Android, Blackberry, Opera Mini, and Windows mobile devices
            var ua = $window['navigator']['userAgent'] || $window['navigator']['vendor'] || $window['opera'];
            return (/iPhone|iPod|iPad|Silk|Android|BlackBerry|Opera Mini|IEMobile/).test(ua);
        }
    }
]);
auth.factory('Auth', ['$rootScope', '$cookies', '$window', '$location', '$translate', 'IsAuthenticated',
                      'Me', 'Logout', 'IsSmartDevice',
function($rootScope, $cookies, $window, $location, $translate, IsAuthenticated,
         Me, Logout, IsSmartDevice){
    var auth = {};
    auth.get = function(key){
        return $cookies.getObject(key) ? $cookies.getObject(key) : null;
    };
    auth.set = function(user){
        $cookies.putObject('weixin', user);
        this.refresh();
    };
    auth.refresh = function(){
        this.user = this.get('weixin');
    };
    auth.remove = function(){
        $cookies.remove('weixin');
        this.refresh();
    };
    auth.user = auth.get('weixin');
    auth.is_authenticated = function(){

        return IsAuthenticated.get().$promise;
    };
    auth.get_user = function() {
        /*The main authentication logic */

        var self = this;
        if (this.user){
            $rootScope.visitor_resolved = true;
            $rootScope.visitor = this.user;
        }
        else {
            var auth_promise = self.is_authenticated();
            auth_promise.then(function(result){
                if (!result.is_authenticated){
                    if (IsSmartDevice()){
                        $window.location.replace("/visitor/");
                    }
                    else{
                        //$window.location.replace("/visitor/?qr=1");
                    }
                }
                else{
                    Me.get(
                        function(success){
                            self.set(success);
                            $rootScope.visitor_resolved = true;
                            $rootScope.visitor = success;
                        },
                        function(error){
                            $translate('AUTHENTICATION.ERROR').then(function (msg) {
                                $rootScope.alerts.push({ type: 'error', msg:  msg});
                            });
                        }
                    );
                }
            });
        }
    };

    auth.logout = function(){
        var self = this;
        Logout.query(function(r){
            $translate('AUTHENTICATION.LOGOUT').then(function (msg) {
                $rootScope.alerts.push({ type: 'info', msg:  msg});
            });
            self.remove();
            $rootScope.visitor_resolved = false;
            $rootScope.visitor = null;
            $location.path('/');
        });
    };

    return auth;
}]);