angular.module('store.services', ['ngResource'])
.constant('store_path', '/account/stores/')
.factory('Store', ['$resource', 'store_path',
    function($resource, store_path){
        return $resource(store_path + ':pk/:action/', {}, {
            query: {method:'GET', params:{pk: null, action: null}, responseType:'json'},
            update: {method: 'PATCH'},
            save: {method: 'POST'},
            remove: {method: 'DELETE'},
            my_store: {method:'GET', params:{pk: null, action: 'my_store'}, responseType:'json'},
            update_photo: {method:'PATCH', params:{action: 'update_photo'}, responseType:'json'},

    });
}])
