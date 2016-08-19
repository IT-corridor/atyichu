angular.module('article.services', ['ngResource'])
.constant('api_path', '/api/v1/')
.factory('Photo1', ['$resource', 'api_path',
    function($resource, api_path){
        return $resource(api_path + 'photo/:pk/:action/', {}, {
            query: {method:'GET', params:{action: 'my_photos'}, responseType:'json', isArray: true},
            my: {method: 'GET', params: {action: 'my_photos'}, responseType: 'json'},       
    });
}]);
// .factory('Kind', ['$resource', 'catalog_path',
//     function($resource, catalog_path){
//         return $resource(catalog_path + 'kinds/:pk/:action/', {}, {
//             query: {method:'GET', params:{pk: null, action: null}, responseType:'json', isArray: true},
//             update: {method: 'PATCH'},
//             save: {method: 'POST'},
//             remove: {method: 'DELETE'},
//     });
// }])
// .factory('Brand', ['$resource', 'catalog_path',
//     function($resource, catalog_path){
//         return $resource(catalog_path + 'brands/:pk/:action/', {}, {
//             query: {method:'GET', params:{pk: null, action: null}, responseType:'json', isArray: true},
//             update: {method: 'PATCH'},
//             save: {method: 'POST'},
//             remove: {method: 'DELETE'},
//     });
// }])
// .factory('Size', ['$resource', 'catalog_path',
//     function($resource, catalog_path){
//         return $resource(catalog_path + 'sizes/:pk/:action/', {}, {
//             query: {method:'GET', params:{pk: null, action: null}, responseType:'json', isArray: true},
//             update: {method: 'PATCH'},
//             save: {method: 'POST'},
//             remove: {method: 'DELETE'},
//     });
// }])
// .factory('Color', ['$resource', 'catalog_path',
//     function($resource, catalog_path){
//         return $resource(catalog_path + 'colors/:pk/:action/', {}, {
//             query: {method:'GET', params:{pk: null, action: null}, responseType:'json', isArray: true},
//             update: {method: 'PATCH'},
//             save: {method: 'POST'},
//             remove: {method: 'DELETE'},
//     });
// }])
// .factory('Commodity', ['$resource', 'catalog_path',
//     function($resource, catalog_path){
//         return $resource(catalog_path + 'commodities/:pk/:action/', {}, {
//             query: {method:'GET', params:{pk: null, action: null}, responseType:'json'},
//             update: {method: 'PATCH', params: {action: null}},
//             save: {method: 'POST'},
//             remove: {method: 'DELETE'},
//             verbose: {method: 'GET', params: {action: 'verbose'}, responseType: 'json'},
//             my: {method: 'GET', params: {action: 'my'}, responseType: 'json', isArray: true},

//     });
// }])
// .factory('Gallery', ['$resource', 'catalog_path',
//     function($resource, catalog_path){
//         return $resource(catalog_path + 'galleries/:pk/:action/', {}, {
//             query: {method:'GET', params:{pk: null, action: null}, responseType:'json', isArray: true},
//             update: {method: 'PATCH', params: {action: null}},
//             save: {method: 'POST'},
//             remove: {method: 'DELETE'},
//             save_many: {method: 'POST', params:{pk: null, action: 'save_many'}, responseType:'json', isArray: true,},
//     });
// }]);