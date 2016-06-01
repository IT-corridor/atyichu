angular.module('photo.services', ['ngResource'])
.constant('source_path', 'snapshot/photo')
.factory('Photo', ['$resource', 'source_path',
    function($resource, source_path){
        return $resource(source_path + '/:pk/', {}, {
            query: {method:'GET', params:{pk: null}, responseType:'json',},
            update: {method: 'PATCH'},
            save: {method: 'POST'},
            remove: {method: 'DELETE'},
    });
}])
