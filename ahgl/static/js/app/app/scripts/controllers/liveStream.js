'use strict';

/**
 * @ngdoc function
 * @name ahgl2App.controller:LiveStreamCtrl
 * @description
 * # LiveStreamCtrl
 * Controller of the ahgl2App
 */
angular.module('ahgl2App')
    .controller('LiveStreamCtrl', function ($scope, $sce, $http) {
        $http.get('http://127.0.0.1:8000/api/streams/?format=json').then(function(response) {
            $scope.liveStream = response.data.channel_name != undefined;
            if (response.data.channel_name) {
                $scope.channel_name = response.data.channel_name;
                $scope.chat_url = $sce.trustAsResourceUrl('http://twitch.tv/chat/embed?channel=' + response.data.channel_name + '&amp;popout_chat=false');
                $scope.live_stream_logo = $sce.trustAsResourceUrl(response.data.image_url);
                $scope.streamTitle = response.data.channel_name;
            }
        });
            
    });