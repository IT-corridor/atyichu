angular.module('common.services', ['ngResource'])
.factory('PopParamString', function(){
    return function (obj, key) {
        if (Object.keys(obj).length == 0){ return '';}
        var str = [];
        for(var p in obj){
            /* Maybe needs to fix */
            if (p != key) {
                str.push(encodeURIComponent(p) + '=' + encodeURIComponent(obj[p]));
            }
        }
        return str.join('&');
    }
})
.factory('GetPageLink',['PopParamString', '$location',
    function(PopParamString, $location){
        return function(){
            var page_link = '#!' +$location.path() + '/?';
            var url_params = PopParamString($location.search(), 'page');
            page_link += url_params ? url_params +'&' : ''
            return page_link;
        }
    }
]);
