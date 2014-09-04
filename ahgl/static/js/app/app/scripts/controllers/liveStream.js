'use strict';

/**
 * @ngdoc function
 * @name ahglApp.controller:LiveStreamCtrl
 * @description
 * # LiveStreamCtrl
 * Controller of the ahglApp
 */
angular.module('ahglApp')
    .controller('LiveStreamCtrl', function ($scope, $sce, liveStreamSvc, urlSvc) {
        liveStreamSvc.fetchStreams()
            .then(function(resp) {
                $scope.liveStream = true;
                $scope.channel_name = resp.channelName;
                $scope.chat_url = $sce.trustAsResourceUrl(urlSvc.chatUrl.replace('{{channelName}}', resp.channelName));
                $scope.live_stream_logo = $sce.trustAsResourceUrl(resp.gameImageUrl);
                $scope.streamTitle = resp.channelName;
            });
    });