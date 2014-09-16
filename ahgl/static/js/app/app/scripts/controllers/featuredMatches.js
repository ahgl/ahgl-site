'use strict';

/**
 * @ngdoc function
 * @name ahglApp.controller:LiveStreamCtrl
 * @description
 * # LiveStreamCtrl
 * Controller of the ahglApp
 */
angular.module('ahglApp')
    .controller('FeaturedMatchesCtrl', function ($scope, $sce, urlSvc, MatchSvc, GamesSvc) {
        $scope.localGamesSvc = GamesSvc;
        $scope.featuredMatchesPresent = false;

        var selectedGameSlug = GamesSvc.getSelectedGameSlug();
        MatchSvc.fetchMatches(selectedGameSlug).then(function(matches) {
                $scope.matches = matches;
                $scope.featuredMatchesPresent = matches.length > 0;
        });

        GamesSvc.fetchGames().then(function(games) {
            $scope.sectionHeaderIconUrl = GamesSvc.getIcon("match", selectedGameSlug);
        });
    });
