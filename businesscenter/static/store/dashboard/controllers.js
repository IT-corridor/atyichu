angular.module('dashboard.controllers', ['ui.load', 'ui.jq'])
    .constant('JQ_CONFIG', {
        plot: ['../static/lib/jquery/flot/jquery.flot.js',
            '../static/lib/jquery/flot/jquery.flot.pie.js',
            '../static/lib/jquery/flot/jquery.flot.resize.js',
            '../static/lib/jquery/flot.tooltip/js/jquery.flot.tooltip.min.js',
            '../static/lib/jquery/flot.orderbars/js/jquery.flot.orderBars.js',
            '../static/lib/jquery/flot-spline/js/jquery.flot.spline.min.js'],
    })
    .controller('CtrlFlotChart', ['$scope', function ($scope) {
        $scope.data = [
            {
                d: [[1, 6.5], [2, 6.5], [3, 7], [4, 8], [5, 7.5], [6, 7], [7, 6.8], [8, 7], [9, 7.2], [10, 7], [11, 6.8], [12, 7]],
                label: 'Following Users',
                color: '#7266ba',
                tick_desc: '%y.0 following groups on %x.0'
            },
            {
                d: [[0, 7], [1, 6.5], [2, 12.5], [3, 7], [4, 9], [5, 6], [6, 11], [7, 6.5], [8, 8], [9, 7]],
                label: 'Following Groups',
                color: '#27c24c',
                tick_desc: '%y.0 following users on %x.0'
            },
            {
                d: [[0, 4], [1, 4.5], [2, 7], [3, 4.5], [4, 3], [5, 3.5], [6, 6], [7, 3], [8, 4], [9, 3], [10, 3]],
                label: 'Likers',
                color: '#23b7e5',
                tick_desc: '%y.0 followers on %x.0'
            }
        ];

        $scope.ticks = [[1, 'Jan'], [2, 'Feb'], [3, 'Mar'], [4, 'Apr'], [5, 'May'],
            [6, 'Jun'], [7, 'Jul'], [8, 'Aug'], [9, 'Sep'], [10, 'Oct'], [11, 'Nov'], [12, 'Dec']]
    }]);
