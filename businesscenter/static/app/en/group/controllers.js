angular.module('group.controllers', ['group.services', 'common.services', 'auth.services'])
.controller('CtrlGroupAdd', ['$scope', '$rootScope','$http',
'$location', '$route', 'Auth', 'MultipartForm',
    function($scope, $rootScope, $http, $location, $route, Auth, MultipartForm) {

        $rootScope.title = 'New group';

        var auth_promise = Auth.is_authenticated();

        auth_promise.then(function(result){
            if (!result.is_authenticated){
                $window.location.replace("/visitor/");
            }
        });

        $scope.add = function() {
            var url = '/api/v1/group/';
            MultipartForm('#group_form', url).then(function(response) {
                $rootScope.alerts.push({ type: 'success', msg: 'Your drone was successfully added!'});
                    $location.path('/');
                },
                function(error) {
                    for (var e in error.data){
                        $rootScope.alerts.push({ type: 'danger', msg: error.data[e]});
                    }
                    $scope.error = error.data;
                }
            );

        };

    }
])
.controller('CtrlGroupList', ['$scope', '$rootScope','$http',
'$location', '$routeParams','GetPageLink' , 'Group',
    function($scope, $rootScope, $http, $location, $routeParams, GetPageLink, Group) {

        $rootScope.title = 'Groups';

        $scope.r = Group.query($routeParams,
            function(success){

                $scope.enough = success.total > 1 ? false : true;
                $scope.page_link = GetPageLink();
                $scope.page = success.current;
                $scope.prev_pages = [];
                $scope.next_pages = [];
                var i = (success.current - 1 > 5) ? success.current - 5: 1;
                var next_lim = (success.total - success.current > 5) ? 5 + success.current : success.total;
                var j = success.current + 1;
                for (i; i < success.current; i++){ $scope.prev_pages.push(i);}
                for (j; j <= next_lim; j++){ $scope.next_pages.push(j);}
            },
            function(error){
                for (var e in error.data){
                        $rootScope.alerts.push({ type: 'danger', msg: error.data[e]});
                    }
                    $scope.error = error.data;
            }
        );

        $scope.get_more = function(){
            $scope.page += 1;
            var params = $routeParams;
            params['page'] = $scope.page;
            Group.query(params, function(success){
                    $scope.r.results = $scope.r.results.concat(success.results);
                    $scope.enough = ($scope.page >= $scope.r.total) ? true : false;
                },
                function(error){
                    $rootScope.alerts.push({ type: 'danger', msg: error.data[e]});
                }
            );
        }
    }
])
.controller('CtrlGroupPhotoList', ['$scope', '$rootScope','$http',
'$location', '$routeParams','GetPageLink' , 'Group',
    function($scope, $rootScope, $http, $location, $routeParams, GetPageLink, Group) {

        $scope.group = Group.get({pk: $routeParams.pk});
        var queryParams = {pk: $routeParams.pk, page: $routeParams.page};
        $scope.r = Group.photo_list(queryParams,
            function(success){
                $rootScope.title = 'Groups photo';
                $scope.enough = success.total > 1 ? false : true;
                $scope.page_link = GetPageLink();
                $scope.page = success.current;
                $scope.prev_pages = [];
                $scope.next_pages = [];
                var i = (success.current - 1 > 5) ? success.current - 5: 1;
                var next_lim = (success.total - success.current > 5) ? 5 + success.current : success.total;
                var j = success.current + 1;
                for (i; i < success.current; i++){ $scope.prev_pages.push(i);}
                for (j; j <= next_lim; j++){ $scope.next_pages.push(j);}
            },
            function(error){
                for (var e in error.data){
                        $rootScope.alerts.push({ type: 'danger', msg: error.data[e]});
                    }
                    $scope.error = error.data;
            }
        );

        $scope.get_more = function(){
            $scope.page += 1;
            var params = {pk: $routeParams.pk, page: $scope.page};
            Group.photo_list(params, function(success){
                    $scope.r.results = $scope.r.results.concat(success.results);
                    $scope.enough = ($scope.page >= $scope.r.total) ? true : false;
                },
                function(error){
                    $rootScope.alerts.push({ type: 'danger', msg: error.data[e]});
                }
            );
        }
    }
])
.controller('CtrlGroupManage', ['$scope', '$rootScope','$http',
'$location', '$route', 'Auth', 'Group',
    function($scope, $rootScope, $http, $location, $route, Auth, Group) {

        $rootScope.title = 'Groups';
    }
]);