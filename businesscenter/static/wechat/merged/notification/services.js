angular.module('notification.services', ['ngResource'])
.constant('source_path', 'api/v1/')
.factory('Notification', ['$resource', 'source_path',
    function($resource, source_path){
        return $resource(source_path + 'notification/:pk/:action/', {}, {
            me: {method:'GET', params:{pk: null, action: 'me'}, responseType:'json', isArray:true},
            reply_notification: {method:'GET', params:{action: 'reply_notification'}, responseType:'json'},
        });
}]);
