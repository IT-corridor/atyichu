angular.module('photo.controllers', ['photo.services'])
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
                                '$window', '$location', 'Photo', 'Comment',
    function($scope, $rootScope, $http, $routeParams, $window, $location,
    Photo, Comment) {
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
            },
            handle_error
        );

        $scope.remove = function(){
            var confirm = $window.confirm('Are you sure you want to clear your cart?');
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

        $scope.update = function(){
            // TODO: implement
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
.controller('CtrlPhotoNewest', ['$scope', '$rootScope','$http',
'$location', '$routeParams','GetPageLink' , 'Photo',
    function($scope, $rootScope, $http, $location, $routeParams, GetPageLink, Photo) {
        $rootScope.title = 'Newest photos';
        $scope.r = Photo.newest(
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
                console.log(error.data);
            }
        );

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
    }
]);