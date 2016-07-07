angular.module('photo.controllers', ['photo.services', 'group.services'])
.controller('CtrlPhotoList', ['$scope', '$rootScope', '$http',
'$location', 'Auth', 'Photo',
    function($scope, $rootScope, $http, $location, Auth, Photo) {
        $rootScope.title = 'Photo List';

        function handle_error(error){
            $rootScope.alerts.push({ type: 'danger',
                    msg: error.data.error});
        }

        $scope.photos = Photo.query(
            function(success){
                $rootScope.alerts.push({ type: 'info',
                    msg: 'Photo list successfully fetched.'});
            },
            handle_error
        );

        $scope.snapshot = function(){
            // TODO: implement screen animation, while waiting for shot
            // First: we set hidden block with "waiting" warn visible.
            Photo.save({},
                function(success){
                    // we can wait for 3 seconds here,
                    $rootScope.alerts.push({ type: 'info', msg: 'Photo was created.'});
                        // hide "waiting" block and reload the path.
                        $location.path('/photo/'+ success.id);
                },
                function(error){
                    $rootScope.alerts.push({ type: 'danger',
                            msg: error.data.error});
                }
            );
        }

    }
])
.controller('CtrlPhotoDetail', ['$scope', '$rootScope', '$http', '$routeParams',
                                '$window', '$location', 'Photo', 'Comment', 'WXI',
    function($scope, $rootScope, $http, $routeParams, $window, $location,
    Photo, Comment,  WXI) {
        $scope.is_owner = false;
        function handle_error(error){
            $rootScope.alerts.push({ type: 'danger', msg: error.data.error});
            $location.path('/photo');
        }

        $scope.photo = Photo.get({pk: $routeParams.pk},
            function(success){
                var title = (success.title) ? success.title : 'Untitled'
                $rootScope.title = 'Photo -' + success.title;
                if ($rootScope.visitor.pk == success.visitor){
                    $scope.is_owner = true;
                }
                var title = (success.title) ? success.title : '品味和格调兼具';
                var photo_desc = (success.description) ? success.description : '大家快来看，秀出你的品味和格调!';
                var descr = title + ': ' + photo_desc;
                WXI.set_on_share(descr, success.photo);
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
            var confirm = $window.confirm('Are you sure you want to remove that photo?');
            if (confirm){
                Photo.remove({pk: $routeParams.pk}, {},
                    function(success){
                        $rootScope.alerts.push({ type: 'info', msg: 'Photo has been deleted!'});
                        $location.path('/photo');
                    },
                    handle_error
                );
            }
        }
        $scope.comment = function(){
            data = {photo: $routeParams.pk, message: $scope.new_message};
                Comment.save(data, function(success){
                    $scope.photo.comments.push(success);
                    $rootScope.alerts.push({ type: 'info', msg: 'Thanks for the comment!'});
                    $scope.new_message = '';
                },
                handle_error
            );
        }
        $scope.like_photo = function(){
            Photo.like({pk: $routeParams.pk},
                function(success){
                    $scope.photo.like = success.like;
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
                                '$window', '$location', 'Photo',
    function($scope, $rootScope, $http, $routeParams, $window, $location, Photo) {
        $rootScope.title = 'Edit Photo Data';
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
                    $rootScope.alerts.push({ type: 'info', msg: 'Data has been updated.'});
                    $location.path('/photo/' + $routeParams.pk);
                },
                handle_error
            );
        }
    }
])
.controller('CtrlPhotoNewest', ['$scope', '$rootScope','$http', '$window',
'$location', '$routeParams','GetPageLink' , 'Photo',
    function($scope, $rootScope, $http, $window, $location, $routeParams, GetPageLink, Photo) {
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

        $rootScope.title = 'Newest photos';
        $rootScope.photo_refer = $location.url();
        $scope.r = Photo.newest(
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
            Photo.newest(params, function(success){
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
                    $scope.r.results[index].like = success.like;
                },
                function(error){
                    $rootScope.alerts.push({ type: 'danger', msg: 'You have liked it already!'});
                }
            );
        }
    }
])
.controller('CtrlPhotoClone', ['$scope', '$rootScope', '$http', '$routeParams',
                                '$window', '$location', 'Photo', 'Group',
    function($scope, $rootScope, $http, $routeParams, $window, $location, Photo, Group) {
        $rootScope.title = 'Clone Photo';

        $scope.photo = Photo.get({pk: $routeParams.pk});
        $scope.r = {};

        $scope.groups = Group.my_short_list();
        $scope.clone = function(){

            Photo.clone({pk: $routeParams.pk}, $scope.r,
                function(success){
                    $rootScope.alerts.push({ type: 'info', msg: 'Photo has been cloned.'});
                    $location.path('/photo/' + success.id);
                },
                function(error){
                    $rootScope.alerts.push({type: 'danger', msg: 'Fail!'});
                }
            );
        }
    }
]);