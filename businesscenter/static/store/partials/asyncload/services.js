angular.module('asyncload.services', [])
.factory('LoadScript', ['$window', '$document', '$q', '$timeout',
function($window, $document, $q, $timeout){
    /* This factory allow to load scripts asynchronous */
    return function (src, is_api) {
        var doc = $document[0];
        var deferred = $q.defer();
        var scripts = doc.querySelectorAll('script');

        $window.init_async = function(){
            /* A small trick for api loaders trick.
            It will be called when the api script (not actual script) will be ready */
            deferred.resolve();
        }
        angular.forEach(scripts,
            function(script) {
                if (script.src == src){
                    deferred.resolve();
                }
            }
        );
        if (deferred.promise.$$state.status == 0){
            var script = doc.createElement('script');
            script.src = src;
            script.onload = function (e) {
                $timeout(function () {
                    if (!is_api){
                        deferred.resolve(e);
                    }

                });
            };
            script.onerror = function (e) {
                $timeout(function () {
                    deferred.reject(e);
                });
            };
            doc.body.appendChild(script);
        }
        return deferred.promise;
    }
}]);