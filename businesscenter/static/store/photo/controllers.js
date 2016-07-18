angular.module('photo.controllers', ['photo.services', 'group.services', 'store.services'])
.controller('CtrlPhotoList', ['$scope', '$rootScope', '$http',
'$location', '$translate', 'Auth', 'Photo',
    function($scope, $rootScope, $http, $location, $translate, Auth, Photo) {
        function handle_error(error){
            $rootScope.alerts.push({ type: 'danger',
                    msg: error.data.error});
        }

        $scope.photos = Photo.query(
            function(success){},
            handle_error
        );

        $scope.snapshot = function(){
            // TODO: implement screen animation, while waiting for shot
            // First: we set hidden block with "waiting" warn visible.
            Photo.save({},
                function(success){
                    // we can wait for 3 seconds here,
                    $translate('PHOTO.LIST.CREATED').then(function (msg) {
                            $rootScope.alerts.push({ type: 'success', msg:  msg});
                    });
                    $location.path('/photo/'+ success.id);
                },
                function(error){
                    $rootScope.alerts.push({ type: 'danger',  msg: error.data.error});
                }
            );
        }

    }
])
.controller('CtrlPhotoDetail', ['$scope', '$rootScope', '$http', '$routeParams',
                                '$window', '$location', '$translate', 'Photo', 'Comment',
                                'Store',
    function($scope, $rootScope, $http, $routeParams, $window, $location, $translate,
    Photo, Comment, Store) {
        $scope.is_owner = false;
        function handle_error(error){
            $rootScope.alerts.push({ type: 'danger', msg: error.data.error});
            $location.path('/photo');
        }

        $scope.photo = Photo.get({pk: $routeParams.pk},
            function(success){
                if ($rootScope.visitor.pk == success.visitor){
                    $scope.is_owner = true;
                }
                if (success.is_store){
                    $scope.store = Store.overview({pk: success.owner.pk});
                }
            },
            handle_error
        );

        $scope.back = function(){
            if ($rootScope.photo_refer){
                $location.url($rootScope.photo_refer);
            }
            else{
                $location.url('/photo/newest');
            }
            console.log($rootScope.photo_refer);
            $rootScope.refer = undefined;
            console.log($rootScope.refer);
        }
        $scope.remove = function(){
            $translate('CONFIRM').then(function (msg) {
                $scope.confirm = $window.confirm(msg);
            });
            if ($scope.confirm){
                Photo.remove({pk: $routeParams.pk}, {},
                    function(success){
                        $translate('PHOTO.DETAIL.DELETED').then(function (msg) {
                            $rootScope.alerts.push({ type: 'danger', msg: msg});
                        });
                        $location.path('/group/'+ $scope.photo.group + '/photo');
                    },
                    handle_error
                );
            }
        }
        $scope.comment = function(){
            data = {photo: $routeParams.pk, message: $scope.new_message};
                Comment.save(data, function(success){
                    $scope.photo.comments.push(success);
                    $scope.new_message = '';
                },
                handle_error
            );
        }
        $scope.like_photo = function(){
            Photo.like({pk: $routeParams.pk},
                function(success){
                    $scope.photo.like_count = success.like_count;
                },
                function(error){
                    $rootScope.alerts.push({ type: 'danger', msg: error.data.error});
                }
            );
        }

        $scope.like_comment = function(index, comment_id){
            Comment.like({pk: comment_id},
                function(success){
                    $scope.photo.comments[index].like = success.like;
                },
                function(error){
                    $rootScope.alerts.push({ type: 'danger', msg: error.data.error});
                }
            );
        }
    }
])
.controller('CtrlPhotoEdit', ['$scope', '$rootScope', '$http', '$routeParams',
                                '$window', '$location', '$translate', 'Photo',
    function($scope, $rootScope, $http, $routeParams, $window, $translate, $location, Photo) {
        function handle_error(error){
            $rootScope.alerts.push({ type: 'danger', msg: error.data.error});
            $location.path('/photo');
        }

        $scope.photo = Photo.get({pk: $routeParams.pk},
            function(success){},
            handle_error
        );


        $scope.update = function(){
            data = {title: $scope.photo.title, description: $scope.photo.description};
            Photo.edit({pk: $routeParams.pk}, data,
                function(success){
                    $translate('PHOTO.EDIT.DATA_UPDATED').then(function (msg) {
                        $rootScope.alerts.push({ type: 'danger', msg: msg});
                    });
                    $location.path('/photo/' + $routeParams.pk);
                },
                handle_error
            );
        }
    }
])
.controller('CtrlPhotoNewest', ['$scope', '$rootScope','$http', '$window',
'$location', '$routeParams', '$translate', 'GetPageLink' , 'Photo', 'title', 'kind',
    function($scope, $rootScope, $http, $window, $location, $routeParams,
    $translate, GetPageLink, Photo, title, kind) {
        // Controller for newest photos and for the liked photos

        $rootScope.title = title;
        var query = (kind === 'newest') ? Photo.newest : Photo.liked_list;

        $scope.enough = false;
        $scope.is_owner = false;

        $scope.new_message = '';

        var window = angular.element($window);

        function scroll_more(){
            if (!$scope.enough && $scope.page != undefined){
                var bodyHeight = this.document.body.scrollHeight;
                if (bodyHeight == (this.pageYOffset + this.innerHeight)){
                    $scope.get_more();
                }
            }
        }
        window.bind('scroll', scroll_more);

        $scope.$on('$destroy', function(e){
            window.unbind('scroll', scroll_more);
        });

        $rootScope.photo_refer = $location.url();
        $scope.r = query(
            function(success){
                $scope.enough = success.total > 1 ? false : true;
                $scope.page_link = GetPageLink();
                $scope.page = success.current;
            },
            function(error){
                console.log(error.data);
            }
        );

        $scope.show_current = function(index){
            $scope.current = index;
            $scope.show_detail = true;
            console.log($scope.current);
        }
        $scope.get_more = function(){
            $scope.page += 1;
            var params = {page: $scope.page};
            query(params, function(success){
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

        $scope.like = function(index, photo_id){
            Photo.like({pk: photo_id},
                function(success){
                    $scope.r.results[index].like_count = success.like_count;
                },
                function(error){
                    $translate('PHOTO.LIST.LIKED').then(function (msg) {
                        $rootScope.alerts.push({ type: 'danger', msg: msg});
                    });
                }
            );
        }
    }
])
.controller('CtrlPhotoClone', ['$scope', '$rootScope', '$http', '$routeParams',
                                '$window', '$location', '$translate', 'Photo', 'Group',
    function($scope, $rootScope, $http, $routeParams, $window, $location,
    $translate, Photo, Group) {
        $scope.wait = false;
        $scope.photo = Photo.get({pk: $routeParams.pk});
        $scope.r = {};

        $scope.groups = Group.my_short_list();
        $scope.clone = function(){
            $scope.wait = true;
            Photo.clone({pk: $routeParams.pk}, $scope.r,
                function(success){
                    $translate('PHOTO.CLONE.CLONED').then(function (msg) {
                        $rootScope.alerts.push({ type: 'success', msg: msg});
                    });
                    $location.path('/photo/' + success.id);
                },
                function(error){
                    $translate('FAIL').then(function (msg) {
                        $rootScope.alerts.push({ type: 'danger', msg: msg});
                    });
                    $scope.wait = false;
                }
            );
        }
    }
]);