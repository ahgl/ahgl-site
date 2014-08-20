'use strict';

/**
 * @ngdoc function
 * @name ahgl2App.controller:LiveStreamCtrl
 * @description
 * # LiveStreamCtrl
 * Controller of the ahgl2App
 */
angular.module('ahgl2App')
    .controller('LiveStreamCtrl', function ($scope, $sce) {
        $scope.liveStream = true;
        $scope.channel_name = 'dubastv';
        $scope.chat_url = $sce.trustAsResourceUrl('http://twitch.tv/chat/embed?channel=dubastv&amp;popout_chat=false');
        $scope.live_stream_logo = '../images/live-stream-game.png';
        $scope.streamTitle = 'Stream Title Here';
    });