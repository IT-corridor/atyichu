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
            MultipartForm('POST', '#group_form', url).then(function(response) {
                $rootScope.alerts.push({ type: 'success', msg: 'Your drone was successfully added!'});
                    // for images
                    //$scope.random = Math.floor((Math.random()*1000));
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
                    for (var e in error.data){
                        $rootScope.alerts.push({ type: 'danger', msg: error.data[e]});
                    }
                    $scope.error = error.data;
                }
            );
        }
    }
])
.controller('CtrlGroupManage', ['$scope', '$rootScope','$http',
'$location', '$routeParams', 'Auth', 'Group', 'MultipartForm', 'Tag',
    function($scope, $rootScope, $http, $location, $routeParams, Auth, Group, MultipartForm, Tag) {

        $rootScope.title = 'Update group';
        $scope.is_owner = false;

        $scope.r = Group.get({pk: $routeParams.pk},
            function(success){
                $scope.data = {title: success.title,
                               description: success.description,
                               is_private: success.is_private};
                if ($rootScope.visitor.pk == success.owner){
                    $scope.is_owner = true;
                }
                if ($rootScope.visitor.pk != success.owner){

                    $rootScope.alerts.push({ type: 'warning',
                        msg: 'You have not enough privileges to manage this group'});
                }
            },
            function(error) {
                // TODO: move that func to partials/common, remove duplicates
                for (var e in error.data){
                    $rootScope.alerts.push({ type: 'danger', msg: error.data[e]});
                }
                $scope.error = error.data;
            }
        );
        $scope.random = Math.floor((Math.random()*1000));

        $scope.update_group = function() {
            Group.update({pk: $routeParams.pk}, $scope.data, function(success){
                    $location.path('/group/'+ $routeParams.pk + '/photo');
                },
                function(error){
                    $rootScope.alerts.push({ type: 'danger', msg: 'Error!'});
                }
            );
        };

        $scope.member_remove = function(member_id){
            Group.member_remove({pk: $routeParams.pk}, {member: member_id},
                function(success){
                    $rootScope.alerts.push({ type: 'info', msg: 'Member has been removed'});
                    remove_item_from_list($scope.r.members, member_id);
                },
                function(error){
                    $rootScope.alerts.push({ type: 'danger', msg: error.data.error });
                }
            );
        }

        $scope.tag_remove = function(tag_id){
            Tag.remove({pk: tag_id},
                function(success){
                    $rootScope.alerts.push({ type: 'info', msg: 'Tag has been removed'});
                    remove_item_from_list($scope.r.tags, tag_id);
                },
                function(error){
                    $rootScope.alerts.push({ type: 'danger', msg: error.data.error });
                }
            );
        }

        function is_member(list, id){
            var i = 0;
            for (i; i < list.length; i++){
                if (list[i].id == member_id){
                    return true;
                }
            }
            return false;
        }

        function remove_item_from_list(list, member_id){
            var i = 0;
            for (i; i < list.length; i++){
                if (list[i].id == member_id){
                    list.splice(i, 1);
                    break;
                }
            }
        }
    }
]);