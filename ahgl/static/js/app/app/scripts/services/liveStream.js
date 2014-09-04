'use strict';

/**
 * @ngdoc function
 * @name ahglApp.services:liveStreamSvc
 * @description
 * # liveStreamSvc
 * Controller of the ahglApp
 */
angular.module('ahglApp')
    .service('liveStreamSvc', function ($sce, $http, $q, urlSvc) {
        
        this.fetchStreams = function () {
            var deferred = $q.defer();
            this.fetchGames()
                .then(function (games) {
                    var endpoints = [];
                    games.data.results.forEach(function (game) {
                        endpoints.push($http.jsonp(urlSvc.streamUrl.replace('{{channelName}}', game.channel_name)));
                    });
                    $q.all(endpoints)
                        .then(function(responses) {
                            responses.some(function (response, index) {
                                if (response.data.stream) {
                                    var game = games.data.results[index],
                                        channelName = game.channel_name,
                                        gameImageUrl = game.live_stream_image_url;
                                    deferred.resolve({ channelName: channelName, gameImageUrl: gameImageUrl });
                                    return true;
                                }
                            });
                        });
                });
            return deferred.promise;
        }  

        this.fetchGames = function () {
            return $http.get($sce.trustAsResourceUrl(urlSvc.gamesUrl));
        } 
    });
