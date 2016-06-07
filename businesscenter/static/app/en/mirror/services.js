angular.module('mirror.services', ['ngResource'])
.constant('source_path', 'snapshot/mirror')
.factory('Mirror', ['$resource', 'source_path',
    function($resource, source_path){
        return $resource(source_path + '/:pk/', {}, {
            query: {method:'GET', params:{pk: null}, responseType:'json', isArray: true},
            update: {method: 'PATCH'},
    });
}])
.factory('MirrorStatus', ['$resource', 'source_path',
    function($resource, source_path){
        return $resource(source_path + '/status/', {}, {
            post: {method:'POST',
            params:{timestamp: '@timestamp',
                    checksum: '@checksum',
                    token: '@token'},
            responseType:'json',},
    });
}])
.factory('MirrorUnlock', ['$resource', 'source_path',
    function($resource, source_path){
        return $resource(source_path + '/unlock/', {}, {
            post: {method:'GET', responseType:'json',},
    });
}]);