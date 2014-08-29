'use strict';

/**
 * @ngdoc overview
 * @name ahglApp
 * @description
 * # ahglApp
 *
 * Main module of the application.
 */
angular
    .module('ahglApp', [
        'ngAnimate',
        'ngCookies',
        'ngResource',
        'ngRoute',
        'ngSanitize',
        'ngTouch'
    ])
    .config(function ($routeProvider) {
        $routeProvider
            .when('/', {
                templateUrl: 'views/main.html',
                controller: 'MainCtrl'
            })
            .otherwise({
                redirectTo: '/'
            });
    })
    .value('urls', {
        gamesUrl: 'http://127.0.0.1:8000/api/games/?format=json',
        streamUrl: 'https://api.twitch.tv/kraken/streams/{{channelName}}?callback=JSON_CALLBACK',
        chatUrl: 'http://twitch.tv/chat/embed?channel={{channelName}}&amp;popout_chat=false'
    });
