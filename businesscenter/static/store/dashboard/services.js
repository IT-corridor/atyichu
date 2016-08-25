angular.module('dashboard.services', ['ngResource'])
    .constant('source_path', '/api/v1/')
    .factory('Dashboard', ['$resource', 'source_path',
        function ($resource, source_path) {
            return $resource(source_path + 'dashboard/:year/:month/:action/', {}, {
                following_groups: {method: 'GET', params: {action: 'following_groups'}, responseType: 'json', isArray: true},
                following_users: {method: 'GET', params: {action: 'following_users'}, responseType: 'json', isArray: true},
            });
        }]);