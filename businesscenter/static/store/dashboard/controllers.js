angular.module('dashboard.controllers', ['dashboard.services', 'ui.load', 'ui.jq'])
    .constant('JQ_CONFIG', {
        plot: ['../static/lib/jquery/flot/jquery.flot.js',
            '../static/lib/jquery/flot/jquery.flot.pie.js',
            '../static/lib/jquery/flot/jquery.flot.resize.js',
            '../static/lib/jquery/flot.tooltip/js/jquery.flot.tooltip.min.js',
            '../static/lib/jquery/flot.orderbars/js/jquery.flot.orderBars.js',
            '../static/lib/jquery/flot-spline/js/jquery.flot.spline.min.js'],
    })
    .controller('CtrlFlotChart', ['$scope', '$routeParams', 'Dashboard',
        function ($scope, $routeParams, Dashboard) {
        $scope.year = 2016;
        $scope.month = 8;
        $scope.years = [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025];
        $scope.months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];

        $scope.date_change = function() {
            refresh();
        }

        $scope.data = [
            {
                label: 'Following Users',
                color: '#7266ba',
                tick_desc: 'You followed %y.0 user(s) on %x.0th'
            },
            {
                label: 'Following Groups',
                color: '#27c24c',
                tick_desc: 'You followed %y.0 group(s) on %x.0th'
            }
        ];

        var query = [Dashboard.following_users, Dashboard.following_groups];
        refresh();

        function refresh() {
            for (var i = 0; i < query.length; i++) {
                $scope.data[i]['d'] = query[i]({year: $scope.year, month: $scope.month}, function(success) {
                    console.log(i);
                });
            }
        }
    }]);
