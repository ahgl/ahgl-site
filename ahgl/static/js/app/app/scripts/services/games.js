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

        // Populate this if we're being loaded from a Django template.
        var selectedGame = (function() {
            if (typeof document === 'undefined') return; // Can't use $location and make sure this is testable.
            var match = document.location.pathname.match(/^\/([^\/]+)\/(videos|casters|teams|schedule|standings)\/?$/);
            if (match) {
                return match[1];
            } else {
                return null;
            }
        })();

        var fetchGames = function () {
            if (gamesPopulated) {
                var deferred = $q.defer();
                deferred.resolve(games);
                return deferred.promise;
            }
            return $http.get(urlSvc.gamesUrl).then(function(resp) {
                games =  _.map(resp.data.results, function(el) {
                    return {tournament_slug: el.tournament_slug,
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

        var selectGame = function(tournamentSlug) {
            selectedGame = tournamentSlug;
        };

        var getSelectedGame = function () {
            return selectedGame;
        };

        var getRandomIcon = function (section) {
            if (games === null) {
                return '';
            }
            if (!(section === 'article' || section === 'match' || section === 'live_stream')) {
                throw Exception('Invalid section provided');
            }
            var numGames = games.length;
            var randomGamePos = Math.floor((Math.random() * numGames));  // 0-based index
            var imageUrl = games[randomGamePos][section + '_section_image_url'];
            return imageUrl;
        };

        return {
            games: games,
            selectGame: selectGame,
            getSelectedGame: getSelectedGame,
            gamesPopulated: gamesPopulated,
            fetchGames: fetchGames,
            getRandomIcon: getRandomIcon
        };
    });
