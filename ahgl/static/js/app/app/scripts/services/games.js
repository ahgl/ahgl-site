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
        var gamesPopulated = false;
        var fetchGames = function () {
            if (gamesPopulated) {
                var promise = deffered.promise;
                promise.then(function(result) {
                    return games;
                });
                return promise;
            }
            return $http.get(urlSvc.gamesUrl).then(function(resp) {    
                games =  _.map(resp.data.results, function(el) {
                    return {slug: el.game_slug,
                            image_url: el.header_image_url,
                            article_section_image_url: el.article_section_image_url,
                            live_stream_section_image_url: el.live_stream_section_image_url,
                            match_section_image_url: el.match_section_image_url};
                });
                gamesPopulated = true;
                return games;
            });
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
            console.log(imageUrl);
            return imageUrl;
        };

        return {games: games, gamesPopulated: gamesPopulated, fetchGames: fetchGames, getRandomIcon: getRandomIcon};    
    });
