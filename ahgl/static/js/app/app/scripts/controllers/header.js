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

        $scope.isGameSelected = GamesSvc.isGameSelected();
        
        $scope.isSelected = function(game) {
            var selectedGameSlug = GamesSvc.getSelectedGameSlug();
            if (!selectedGameSlug) {
                return false;
            }
            return game.slug === selectedGameSlug;
        };

        $scope.getImageUrl = function(game) {
            var imageUrl = game.image_url;
            if ($scope.isSelected(game)) {
                imageUrl = imageUrl.replace('.png', '');
                return imageUrl + '-highlight.png';
            }
            return imageUrl;
        };
    });
