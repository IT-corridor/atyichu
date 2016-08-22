angular.module('photo.controllers', ['photo.services', 'group.services',
'store.services', 'common.services', 'tencent'])
.controller('CtrlPhotoList', ['$scope', '$rootScope','$http', '$window',
'$location', '$routeParams', 'GetPageLink' , 'Photo', 'WindowScroll',
    function($scope, $rootScope, $http, $window, $location, $routeParams,
    GetPageLink, Photo, WindowScroll) {
        // Controller for searching photos
        // TODO: Merge with newest controller

        $scope.enough = false;
        $scope.is_owner = false;

        $scope.new_message = '';


        $rootScope.photo_refer = $location.url();
        $scope.r = Photo.query($routeParams,
            function(success){
                $scope.enough = success.total > 1 ? false : true;
                $scope.page_link = GetPageLink();
                $scope.page = success.current;
            },
            function(error){
                console.log(error.data);
            }
        );

        $scope.get_more = function(){
            $scope.page += 1;
            var params = {page: $scope.page, q: $routeParams.q};
            Photo.query(params, function(success){
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
        };

        WindowScroll($scope, $scope.get_more);

        $scope.like = function(index, photo_id){
            Photo.like({pk: photo_id},
                function(success){
                    $scope.r.results[index].like_count = success.like_count;
                },
                function(error){
                    $rootScope.alerts.push({ type: 'danger', msg: 'Already liked'});
                }
            );
        };

        $scope.snapshot = function(){
            // TODO: implement screen animation, while waiting for shot
            // First: we set hidden block with "waiting" warn visible.
            Photo.save({},
                function(success){
                    // we can wait for 3 seconds here,
                    $rootScope.alerts.push({ type: 'success', msg:  'Photo created.'});
                    $location.path('/photo/'+ success.id);
                },
                function(error){
                    $rootScope.alerts.push({ type: 'danger',  msg: error.data.error});
                }
            );
        };
    }
])
.controller('CtrlPhotoDetail', ['$scope', '$rootScope', '$http', '$routeParams',
                                '$window', '$location', 'Photo', 'Comment',
                                'WXI', 'Store', 'WindowScroll',
    function($scope, $rootScope, $http, $routeParams, $window, $location,
    Photo, Comment,  WXI, Store, WindowScroll) {
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
                if (success.is_store === true){
                    $scope.store = Store.overview({pk: success.owner.pk},
                        function (success){
                            create_empty_array(success);
                        }
                    );
                }
                var title = (success.title) ? success.title : '品味和格调兼具';
                var photo_desc = (success.description) ? success.description : '大家快来看，秀出你的品味和格调!';
                var descr = title + ': ' + photo_desc;
                WXI.set_on_share(descr, success.photo);
            },
            handle_error
        );

        $scope.read_article = function(article_id) {
            $location.path('/article/' + article_id);
        }
        
        /* "Similar photos block. Need to be cleaned */

        $scope.enough = false;
        $scope.r = Photo.similar({pk: $routeParams.pk}, function(success){
            $scope.page = success.current;
            $scope.enough = ($scope.page >= success.total) ? true : false;
        });

        $scope.get_more = function(){
            $scope.page += 1;
            Photo.similar({pk: $routeParams.pk, page: $scope.page}, function(success){
                    $scope.r.results = $scope.r.results.concat(success.results);
                    $scope.enough = ($scope.page >= $scope.r.total) ? true : false;
                }
            );
        }
        WindowScroll($scope, $scope.get_more);
        /* End of similar photos block */

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
                    $rootScope.alerts.push({ type: 'info', msg: 'Thanks for the comment!'});
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

        function create_empty_array(obj){
            var len = obj.overview.length;
            var empty = 4 - len;
            obj.empty_array = [];
            var l = 0;
            for (l; l < empty; l++){ obj.empty_array.push(l);}
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
'WindowScroll', 'Visitor', 'IsMember', 'RemoveItem', 'title', 'kind',
    function($scope, $rootScope, $http, $window, $location, $routeParams,
    GetPageLink, Photo, WindowScroll, Visitor, IsMember, RemoveItem, title, kind) {
        // Controller for newest photos and for the liked photos

        $rootScope.title = title;
        var query = (kind === 'newest') ? Photo.newest : Photo.liked_list;
        if (kind === 'article')
            query = Photo.query;
        
        $scope.enough = false;
        $scope.is_owner = false;

        $scope.new_message = '';
        $rootScope.title = 'Newest photos';
        $rootScope.photo_refer = $location.url();
        $scope.followed = Visitor.get_follow_users();

        $scope.followed.$promise.then(function(list){

            $scope.r = query(
                function(success){
                    $scope.enough = success.total > 1 ? false : true;
                    $scope.page_link = GetPageLink();
                    $scope.page = success.current;
                    var i = 0, l = success.results.length;
                    for (i; i < l; i++){
                        success.results[i]['owner_followed'] = IsMember(list.results, success.results[i].visitor, 'pk');
                        success.results[i]['creator_followed'] = IsMember(list.results, success.results[i].creator, 'pk');
                    };
                },
                function(error){
                    console.log(error.data);
                }
            );
        });


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
        };
        WindowScroll($scope, $scope.get_more);

        $scope.like = function(index, photo_id){
            Photo.like({pk: photo_id},
                function(success){
                    $scope.r.results[index].like_count = success.like_count;
                },
                function(error){
                    $rootScope.alerts.push({ type: 'danger', msg: 'You have liked it already!'});
                }
            );
        }

        $scope.follow_user = function(user_id, index, is_creator) {
            Visitor.follow_user({pk: user_id},
                function(success){
                    $scope.followed.results.push({'pk': user_id});
                    if (is_creator){
                        $scope.r.results[index]['creator_followed'] = true;
                    }
                    else {
                        $scope.r.results[index]['owner_followed'] = true;
                    }
                    console.log($scope.followed);
                },
                function(error){
                    $rootScope.alerts.push({ type: 'danger', msg: 'You have followed the user already!'});
                }
            );
        };

        $scope.unfollow_user = function(user_id, index, is_creator) {
            Visitor.unfollow_user({pk: user_id},
                function(success){
                    RemoveItem($scope.followed.results, user_id, 'pk');
                    if (is_creator){
                        $scope.r.results[index]['creator_followed'] = false;
                    }
                    else {
                        $scope.r.results[index]['owner_followed'] = false;
                    }
                    console.log($scope.followed);
                },
                function(error){
                    //$rootScope.alerts.push({ type: 'danger', msg: 'You have followed it already!'});
                }
            );
        }

    }
])
.controller('CtrlPhotoClone', ['$scope', '$rootScope', '$http', '$routeParams',
                                '$window', '$location', 'Photo', 'Group',
    function($scope, $rootScope, $http, $routeParams, $window, $location, Photo, Group) {
        $rootScope.title = 'Clone Photo';
        $scope.wait = false;
        $scope.photo = Photo.get({pk: $routeParams.pk});
        $scope.r = {};

        $scope.groups = Group.my_short_list();
        $scope.clone = function(){
            $scope.wait = true;
            Photo.clone({pk: $routeParams.pk}, $scope.r,
                function(success){
                    $rootScope.alerts.push({ type: 'info', msg: 'Photo has been cloned.'});
                    $location.path('/photo/' + success.id);
                },
                function(error){
                    $rootScope.alerts.push({type: 'danger', msg: 'Fail!'});
                    $scope.wait = false;
                }
            );
        }
    }
]);