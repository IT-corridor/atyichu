angular.module('dashboard.controllers', ['dashboard.services', 'ui.load', 'ui.jq'])
    .constant('JQ_CONFIG', {
        plot: ['../static/lib/jquery/flot/jquery.flot.js',
            '../static/lib/jquery/flot/jquery.flot.pie.js',
            '../static/lib/jquery/flot/jquery.flot.resize.js',
            '../static/lib/jquery/flot.tooltip/js/jquery.flot.tooltip.min.js',
            '../static/lib/jquery/flot.orderbars/js/jquery.flot.orderBars.js',
            '../static/lib/jquery/flot-spline/js/jquery.flot.spline.min.js'],
    })
    .controller('CtrlFlotChart', ['$scope', '$routeParams', 'Dashboard', function ($scope, $routeParams, Dashboard) {
        $scope.year = '2016';
        $scope.month = '08';

        $scope.data = [
            {
                label: 'Following Users',
                color: '#7266ba',
                tick_desc: '%y.0 following groups on %x.0'
            },
            {
                label: 'Following Groups',
                color: '#27c24c',
                tick_desc: '%y.0 following users on %x.0'
            }
        ];

        var query = [Dashboard.following_users, Dashboard.following_groups];
        for (var i=0; i<query.length; i++) {
            $scope.data[i]['d'] = query[i]({year: $scope.year, month: $scope.month});
        }
    }]);
