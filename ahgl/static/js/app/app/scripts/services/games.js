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
        var selectedGameSlug = null;

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

        var selectGameSlug = function(gameSlug) {
            selectedGameSlug = gameSlug;
        };

        var getSelectedGameSlug = function () {
            return selectedGameSlug;
        };

        var isGameSelected = function() {
            return getSelectedGameSlug() !== null;
        };

        var getIcon = function(section, gameSlug) {
            if (games === null) {
                return "";
            }

            if (!(section === 'article' || section === 'match' || section === 'live_stream')) {
                throw Exception('Invalid section provided');
            }

            if (typeof gameSlug === 'undefined' || gameSlug === null) {
                return getRandomIcon(section);
            }
            var game = _.find(games, function(g) { 
                return g.slug === gameSlug;
            });
            return game[section + '_section_image_url'];
        };

        var getRandomIcon = function (section) {
            var numGames = games.length;
            var randomGamePos = Math.floor((Math.random() * numGames));  // 0-based index
            var imageUrl = games[randomGamePos][section + '_section_image_url'];
            console.log(imageUrl);
            return imageUrl;
        };

        return {games: games, 
                selectGameSlug: selectGameSlug,
                getSelectedGameSlug: getSelectedGameSlug,
                isGameSelected: isGameSelected,
                fetchGames: fetchGames,
                getIcon: getIcon};    
    });
