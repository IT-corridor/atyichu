angular.module('user.services', ['ngResource'])
.constant('user_path', 'visitor/profile/')
.factory('User', ['$resource', 'user_path',
    function($resource, user_path){
        return $resource(user_path + ':pk/:action/', {}, {
            query: {method:'GET', params:{pk: null}, responseType:'json'},
            me: {method:'GET', params:{pk: null, action: 'me'}, responseType:'json'},
            update: {method: 'PATCH'},
            save: {method: 'POST'},
            edit: {method: 'PATCH', params: {action: 'edit'}, responseType: 'json'},
            change_password: {method: 'POST', params: {action: 'change_password'}, responseType: 'json'},
            login: {method: 'POST', params: {action: 'login'}, responseType: 'json'},
    });
}]);
