'use strict';

/**
 * @ngdoc function
 * @name ahglApp.controller:HeaderCtrl
 * @description
 * # HeaderCtrl
 * Controller of the ahglApp
 */
angular.module('ahglApp')
    .controller('HeaderCtrl', function ($scope, GamesSvc) {

        GamesSvc.fetchGames().then(function(games) {
            $scope.games = games;
        });

        $scope.$watch('GamesSvc.getSelectedGame()', function() {
            $scope.selectedGame = GamesSvc.getSelectedGame();
            $scope.isGameSelected = $scope.selectedGame !== null;
        });

        $scope.tabs = [
            { title: 'Videos', slug: 'videos' },
            { title: 'Casters', slug: 'casters' },
            { title: 'Teams', slug: 'teams' },
            { title: 'Schedule', slug: 'schedule' },
            { title: 'Standings', slug: 'videos' }
        ];

        // Populate this if we're being loaded from a Django template.
        $scope.selectedTab = (function() {
            if (typeof document === 'undefined') return; // Can't use $location and make sure this is testable.
            var match = document.location.pathname.match(/^\/([^\/]+)\/(\w+)\/?$/);
            if (match) {
                return match[2];
            } else {
                return null;
            }
        })();

        $scope.isSelected = function(game) {
            var selectedGame = GamesSvc.getSelectedGame();
            if (!selectedGame) {
                return false;
            }
            return game.slug === selectedGame;
        };

        $scope.getImageUrl = function(game) {
            var imageUrl = game.image_url;
            if ($scope.isSelected(game)) {
                imageUrl = imageUrl.replace('.png', '');
                return imageUrl + '-highlight.png';
            }
            return imageUrl;
        };

        $scope.getSelectedIconUrl = function(game) {
            if ($scope.isSelected(game)) {
                var imageUrl = game.image_url;
                imageUrl = imageUrl.replace('.png', '');
                return imageUrl + '-active.png';
            }
            return null;
        };
    });
