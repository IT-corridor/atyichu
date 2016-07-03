angular.module('weixinapi', [])
.factory('Signature', ['$resource',
    function($resource){
        return $resource('api/v1/signature', {}, {
            get: {method:'GET', responseType:'json'},
        });
    }
])
.factory('WXI', ['$rootScope', '$window', '$q', 'Signature',
function($rootScope, $window, $q, Signature){
    var loc = $window.location.href;
    var defer = $q.defer();
    var WXI = {};

    Signature.get({location: loc}, function (success){
        var tmp;
        tmp = wx.config({
            debug: false,
            appId: success.appId,
            timestamp: success.timestamp,
            nonceStr: success.noncestr,
            signature: success.signature,
            jsApiList: ['getLocation']
        });

        defer.resolve(tmp);

        wx.error(function(res){
            $rootScope.error = res;
            $rootScope.$apply();
        });
    });

    WXI.get_location = function(){
        var inner = $q.defer();
        defer.promise.then(function success(){

            wx.getLocation({
                success: function (res) {
                    inner.resolve({latitude: res.latitude, longitude: res.longitude});
                }
            });
        });
        return inner.promise;
    };
    return WXI;
}]);
