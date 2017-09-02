/**
 * @author v.lugovksy
 * created on 16.12.2015
 */
(function () {
    'use strict';

    angular.module('BlurAdmin.pages.dashboard')
        .controller('CourseChartCtrl', CourseChartCtrl);

    /** @ngInject */
    function CourseChartCtrl($scope, baConfig, colorHelper, lodash, Course) {

        $scope.transparent = baConfig.theme.blur;
        var dashboardColors = baConfig.colors.gradation;

        Course.list()
            .then(function (response, status) {
                $scope.total = response.data.count;
                var courses = response.data.results;

                courses = lodash.groupBy(courses, function (course) {
                    return course.status;
                });

                if (!courses.hasOwnProperty('Proposed')) {
                    courses["Proposed"] = [];
                }

                if (!courses.hasOwnProperty('In Progress')) {
                    courses["In Progress"] = [];
                }

                if (!courses.hasOwnProperty('Published')) {
                    courses["Published"] = [];
                }

                $scope.doughnutData = [
                    {
                        value: courses["Proposed"].length,
                        color: dashboardColors.dark,
                        highlight: colorHelper.shade(dashboardColors.lightest, 15),
                        label: 'Proposed',
                        percentage: courses["Proposed"].length * 100 / $scope.total,
                        order: 1
                    }, {
                        value: courses["In Progress"].length,
                        color: dashboardColors.darker,
                        highlight: colorHelper.shade(dashboardColors.lightDark, 15),
                        label: 'In Progress',
                        percentage: courses["In Progress"].length * 100 / $scope.total,
                        order: 2,
                    }, {
                        value: courses["Published"].length,
                        color: dashboardColors.darkest,
                        highlight: colorHelper.shade(dashboardColors.dark, 15),
                        label: 'Published',
                        percentage: courses["Published"].length * 100 / $scope.total,
                        order: 3,
                    },

                    // {
                    //     value: 1200,
                    //     color: dashboardColors.silverTree,
                    //     highlight: colorHelper.shade(dashboardColors.silverTree, 15),
                    //     label: 'Direct Traffic',
                    //     percentage: 38,
                    //     order: 2,
                    // }, {
                    //     value: 400,
                    //     color: dashboardColors.gossip,
                    //     highlight: colorHelper.shade(dashboardColors.gossip, 15),
                    //     label: 'Ad Campaigns',
                    //     percentage: 17,
                    //     order: 0,
                    // },
                ];

                var ctx = document.getElementById('course-area').getContext('2d');
                window.courses = new Chart(ctx).Doughnut($scope.doughnutData, {
                    segmentShowStroke: false,
                    percentageInnerCutout: 64,
                    responsive: true
                });

            });


    }
})();
