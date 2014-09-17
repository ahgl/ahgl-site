'use strict';

/**
 * @ngdoc function
 * @name ahglApp.services:liveStreamSvc
 * @description
 * # liveStreamSvc
 * Controller of the ahglApp
 */
angular.module('ahglApp')
    .service('liveStreamSvc', function ($sce, $http, $q, urlSvc, GamesSvc) {
        
        this.fetchStreams = function (gameFilter) {
            var deferred = $q.defer();

            GamesSvc.fetchGames()
                .then(function (games) {
                    var endpoints = [];
                    if (gameFilter) {
                        games = _.filter(games, function(g){ return g.slug === gameFilter});
                    }

                    games.forEach(function (game) {
                        endpoints.push($http.jsonp(urlSvc.streamUrl.replace('{{channelName}}', game.channel_name)));
                    });
                    $q.all(endpoints)
                        .then(function(responses) {
                            responses.some(function (response, index) {
                                if (response.data.stream) {
                                    var game = games[index],
                                        channelName = game.channel_name,
                                        gameImageUrl = game.section_image_url;
                                    deferred.resolve({ channelName: channelName,
                                                       gameImageUrl: gameImageUrl,
                                                       username: response.data.stream.channel.display_name,
                                                       gameName: response.data.stream.game});
                                    return true;
                                }
                            });
                        });
                });
            return deferred.promise;
        };
    });
