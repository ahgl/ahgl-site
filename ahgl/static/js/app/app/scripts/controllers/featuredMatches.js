'use strict';

/**
 * @ngdoc function
 * @name ahglApp.controller:LiveStreamCtrl
 * @description
 * # LiveStreamCtrl
 * Controller of the ahglApp
 */
angular.module('ahglApp')
    .controller('FeaturedMatchesCtrl', function ($scope, $sce, urlSvc, MatchSvc) {
        MatchSvc.fetchMatches().then(function(matches) {
                $scope.matches = matches;
            });
    });
