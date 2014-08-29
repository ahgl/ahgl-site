'use strict';

/**
 * @ngdoc function
 * @name ahglApp.services:headerSvc
 * @description
 * # headerSvc
 * Controller of the ahglApp
 */
angular.module('ahglApp')
    .service('urlSvc', function (ENV) {
        
        this.carouselUrl = ENV.apiEndpoint + '/api/carousel/?format=json';
        this.headerInfoUrl = ENV.apiEndpoint + '/api/header/?format=json';
        this.gamesUrl = ENV.apiEndpoint + '/api/games/?format=json';
        this.streamUrl = 'https://api.twitch.tv/kraken/streams/{{channelName}}?callback=JSON_CALLBACK';
        this.chatUrl = 'http://twitch.tv/chat/embed?channel={{channelName}}&amp;popout_chat=false';
    });
