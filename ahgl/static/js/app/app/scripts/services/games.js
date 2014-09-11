'use strict';

/**
 * @ngdoc function
 * @name ahglApp.services:gamesSvc
 * @description
 * # gamesSvc
 * Controller of the ahglApp
 */
angular.module('ahglApp')
    .service('GamesSvc', function ($sce, $http, urlSvc) {
        var games = null;
        var fetchGames = function () {
            if (games !== null) {
                return games;
            }
            return $http.get(urlSvc.gamesUrl).then(function(resp) {    
                games =  _.map(resp.data.results, function(el) {
                    return {slug: el.game_slug, image_url: el.header_image_url};
                });
                return games;
            });
        };

        var getRandomIcon = function (section) {
            return "bloom.jpg"
        };

        return {games: games, fetchGames: fetchGames, getRandomIcon: getRandomIcon};    
    });
