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

        function handle_error(error){
            $rootScope.alerts.push({ type: 'danger', msg: error.data.error});
            $location.path('/photo');
        }

        $scope.photo = Photo.get({pk: $routeParams.pk},
            function(success){
                var title = (success.title) ? success.title : 'Untitled'
                $rootScope.title = 'Photo -' + success.title;
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
    }
])
.controller('CtrlPhotoEdit', ['$scope', '$rootScope', '$http', '$routeParams',
                                '$window', '$location', 'Photo', 'PhotoUpdate',
    function($scope, $rootScope, $http, $routeParams, $window, $location,
    Photo, PhotoUpdate) {
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
            PhotoUpdate.update({pk: $routeParams.pk}, data,
                function(success){
                    $rootScope.alerts.push({ type: 'info', msg: 'Data has been updated.'});
                    $location.path('/photo/' + $routeParams.pk);
                },
                handle_error
            );
        }
    }
]);