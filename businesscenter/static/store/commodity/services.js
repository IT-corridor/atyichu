angular.module('commodity.services', ['ngResource'])
.constant('catalog_path', '/catalog/')
.factory('Category', ['$resource', 'catalog_path',
    function($resource, catalog_path){
        return $resource(catalog_path + 'categories/:pk/:action/', {}, {
            query: {method:'GET', params:{pk: null, action: null}, responseType:'json', isArray: true},
            update: {method: 'PATCH'},
            save: {method: 'POST'},
            remove: {method: 'DELETE'},
    });
}])
.factory('Kind', ['$resource', 'catalog_path',
    function($resource, catalog_path){
        return $resource(catalog_path + 'kinds/:pk/:action/', {}, {
            query: {method:'GET', params:{pk: null, action: null}, responseType:'json', isArray: true},
            update: {method: 'PATCH'},
            save: {method: 'POST'},
            remove: {method: 'DELETE'},
    });
}])
.factory('Brand', ['$resource', 'catalog_path',
    function($resource, catalog_path){
        return $resource(catalog_path + 'brands/:pk/:action/', {}, {
            query: {method:'GET', params:{pk: null, action: null}, responseType:'json', isArray: true},
            update: {method: 'PATCH'},
            save: {method: 'POST'},
            remove: {method: 'DELETE'},
    });
}])
.factory('Size', ['$resource', 'catalog_path',
    function($resource, catalog_path){
        return $resource(catalog_path + 'sizes/:pk/:action/', {}, {
            query: {method:'GET', params:{pk: null, action: null}, responseType:'json', isArray: true},
            update: {method: 'PATCH'},
            save: {method: 'POST'},
            remove: {method: 'DELETE'},
    });
}])
.factory('Color', ['$resource', 'catalog_path',
    function($resource, catalog_path){
        return $resource(catalog_path + 'colors/:pk/:action/', {}, {
            query: {method:'GET', params:{pk: null, action: null}, responseType:'json', isArray: true},
            update: {method: 'PATCH'},
            save: {method: 'POST'},
            remove: {method: 'DELETE'},
    });
}])
.factory('Commodity', ['$resource', 'catalog_path',
    function($resource, catalog_path){
        return $resource(catalog_path + 'commodities/:pk/:action/', {}, {
            query: {method:'GET', params:{pk: null, action: null}, responseType:'json'},
            update: {method: 'PATCH'},
            save: {method: 'POST'},
            remove: {method: 'DELETE'},
    });
}]);