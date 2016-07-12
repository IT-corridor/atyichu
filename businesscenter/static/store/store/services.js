angular.module('store.services', ['ngResource'])
.constant('source_path', '/account/stores/')
.factory('Store', ['$resource', 'source_path',
    function($resource, source_path){
        return $resource(source_path + ':pk/:action/', {}, {
            query: {method:'GET', params:{pk: null, action: null}, responseType:'json'},
            update: {method: 'PATCH'},
            save: {method: 'POST'},
            remove: {method: 'DELETE'},
            my_store: {method:'GET', params:{pk: null, action: 'my_store'}, responseType:'json'},

    });
}])
