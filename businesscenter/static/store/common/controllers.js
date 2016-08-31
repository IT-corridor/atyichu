angular.module('common.controllers', ['auth.services', 'ngCookies'])
.controller('CtrlHome', ['$scope', '$rootScope','$http', '$cookies',
'$location', '$route', '$window', 'Auth', 'Logout',
    function($scope, $rootScope, $http, $cookies, $location, $route, $window, Auth, Logout) {

        $rootScope.title = 'The First Page';

    }
]).controller('CtrlChat', ['$scope', '$rootScope','$http', '$cookies',
'$location', '$route', '$window', 'Auth', 'Logout',
    function($scope, $rootScope, $http, $cookies, $location, $route, $window, Auth, Logout) {
        if (chat_initialized) {
            // setup scroll stickerpipe module
            setupStickerPipe();

            // load chat dialogs
            retrieveChatDialogs();

            // setup message listeners
            setupAllListeners();

            // setup scroll events handler
            setupMsgScrollHandler();
        }
    }
]);