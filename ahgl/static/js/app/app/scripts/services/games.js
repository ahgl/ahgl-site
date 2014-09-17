'use strict';

/**
 * @ngdoc function
 * @name ahglApp.services:gamesSvc
 * @description
 * # gamesSvc
 * Controller of the ahglApp
 */
angular.module('ahglApp')
    .service('GamesSvc', function ($sce, $http, $q, $route, urlSvc) {
        var games = null;
        var gamesPopulated = false;
        var selectedGame = null;

        var fetchGames = function () {
            if (gamesPopulated) {
                var deferred = $q.defer();
                deferred.resolve(games);
                return deferred.promise;
            }
            return $http.get(urlSvc.gamesUrl).then(function(resp) {
                games =  _.map(resp.data.results, function(el) {
                    return {slug: el.slug,
                            image_url: el.header_image_url,
                            article_section_image_url: el.article_section_image_url,
                            live_stream_section_image_url: el.live_stream_section_image_url,
                            match_section_image_url: el.match_section_image_url,
                            channel_name: el.channel_name};
                });
                gamesPopulated = true;
                return games;
            });
        };

        var selectGame = function(gameSlug) {
            selectedGame = gameSlug;
        };

        var getSelectedGame = function () {
            return selectedGame;
        };

        var getRandomIcon = function (section) {
            if (games === null) {
                return "";
            }
            if (!(section === 'article' || section === 'match' || section === 'live_stream')) {
                throw Exception('Invalid section provided');
            }
            var numGames = games.length;
            var randomGamePos = Math.floor((Math.random() * numGames));  // 0-based index
            var imageUrl = games[randomGamePos][section + '_section_image_url'];
            return imageUrl;
        };

        return {games: games, selectGame: selectGame, getSelectedGame: getSelectedGame, gamesPopulated: gamesPopulated, fetchGames: fetchGames, getRandomIcon: getRandomIcon};
    });
