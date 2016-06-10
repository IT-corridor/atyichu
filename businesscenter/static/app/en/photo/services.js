angular.module('photo.services', ['ngResource'])
.constant('source_path', 'api/v1/')
.factory('Photo', ['$resource', 'source_path',
    function($resource, source_path){
        return $resource(source_path + 'photo/:pk/', {}, {
            query: {method:'GET', params:{pk: null}, responseType:'json', isArray: true},
            update: {method: 'PATCH'},
            save: {method: 'POST'},
            remove: {method: 'DELETE'},
    });
}])
.factory('PhotoUpdate', ['$resource', 'source_path',
    function($resource, source_path){
        return $resource(source_path + 'photo/:pk/edit/', {}, {
            update: {method: 'PATCH'},
    });
}])
.factory('Comment', ['$resource', 'source_path',
    function($resource, source_path){
        return $resource(source_path + 'comment/:pk/', {}, {
            query: {method:'GET', params:{pk: null}, responseType:'json', isArray: true},
            update: {method: 'PATCH'},
            save: {method: 'POST'},
            remove: {method: 'DELETE'},
    });
}]);
