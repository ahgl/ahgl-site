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
        'config',
        'ngAnimate',
        'ngCookies',
        'ngResource',
        'ngRoute',
        'ngSanitize',
        'ngTouch',
        'angular-carousel'
    ])
    .config(function ($routeProvider) {
        $routeProvider
            .when('/', {
                templateUrl: 'views/main.html',
                controller: 'MainCtrl'
            })
            .when('/tournament/:tournamentSlug', {
                templateUrl: 'views/main.html',
                controller: 'GameCtrl'
            })
            .otherwise({
                redirectTo: '/'
            });
    });
