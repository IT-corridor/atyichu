angular.module('group.services', ['ngResource'])
.constant('source_path', 'api/v1/')
.factory('Group', ['$resource', 'source_path',
    function($resource, source_path){
        return $resource(source_path + 'group/:pk/:action/', {}, {
            query: {method:'GET', params:{pk: null, action: null}, responseType:'json'},
            update: {method: 'PATCH'},
            save: {method: 'POST'},
            remove: {method: 'DELETE'},
            photo_list: {method:'GET', params:{action: 'photo_list'}, responseType:'json'},
            member_add: {method:'POST', params:{action: 'member_add'}, responseType:'json'},
            member_remove: {method:'POST', params:{action: 'member_remove'}, responseType:'json'},
            tag_create: {method:'POST', params:{action: 'tag_create'}, responseType:'json'},
            visitor_list: {method:'GET', params:{pk: null, action: 'visitor_list'},
                           responseType:'json', isArray:true},
            my: {method:'GET', params:{pk: null, action: 'my_groups'}, responseType:'json'},
            my_short_list: {method:'GET', params:{pk: null, action: 'my_groups_short'},
                responseType:'json', isArray: true},
    });
}])
.factory('GroupPhoto', ['$resource', 'source_path',
    function($resource, source_path){
        return $resource(source_path + 'group-photo/:pk/', {}, {
            update: {method: 'PATCH'},
            remove: {method: 'DELETE'},
    });
}])
.factory('Tag', ['$resource', 'source_path',
    function($resource, source_path){
        return $resource(source_path + 'tag/:pk/:action/', {}, {
            update: {method: 'PATCH'},
            remove: {method: 'DELETE'},
    });
}])
.factory('Member', ['$resource', 'source_path',
    function($resource, source_path){
        return $resource(source_path + 'member/short_list/', {}, {
            query: {method:'GET', responseType:'json', isArray:true},
    });
}])
.factory('MultipartForm', ['$http', function ($http){
    return function(method, form_id, url){
        if (form_id){
            var form = document.querySelector(form_id);
            var formData = new FormData(form);
        }
        else{
            var formData = null;
        }
        var req = {
            method: method,
            url: url,
            headers: {'Content-Type': undefined, 'X-Requested-With': 'XMLHttpRequest'},
            data: formData,
        };
        return $http(req);
    }
}]);

/*Example of MultipartForm usage:
    var url = '/api/v1/group/';
    var url2 = '/api/v1/group/1/create_photo/'
    MultipartForm('#group_form', url).then(function(response) {
        $rootScope.alerts.push({ type: 'success', msg: 'Your drone was successfully added!'});
            $location.path('/group');
        },
        function(response) {
            $scope.error = response.data;
        }
    );
*/