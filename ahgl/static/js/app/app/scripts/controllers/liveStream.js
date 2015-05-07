'use strict';

/**
 * @ngdoc function
 * @name ahglApp.controller:LiveStreamCtrl
 * @description
 * # LiveStreamCtrl
 * Controller of the ahglApp
 */
angular.module('ahglApp')
    .controller('LiveStreamCtrl', function ($scope, $sce, liveStreamSvc, urlSvc, GamesSvc) {
        
        var selectedGame = GamesSvc.getSelectedGame();
                
        liveStreamSvc.fetchStreams(selectedGame)
            .then(function(resp) {
                $scope.liveStream = true;
                $scope.channel_name = resp.channelName;
                $scope.chat_url = $sce.trustAsResourceUrl(urlSvc.chatUrl.replace('{{channelName}}', resp.channelName));
                $scope.live_stream_logo = $sce.trustAsResourceUrl(resp.gameImageUrl);
                $scope.streamTitle = resp.streamTitle;
                $scope.gameName = resp.gameName;
                $scope.username = resp.username;
            });

        GamesSvc.fetchGames().then(function(games) {
            $scope.sectionHeaderIconUrl = GamesSvc.getIcon("live_stream", selectedGame);
        });

    });