'use strict';

/**
 * @ngdoc function
 * @name ahglApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the ahglApp
 */
angular.module('ahglApp')
    .controller('GameCtrl', function ($routeParams, GamesSvc) {
        GamesSvc.selectGame($routeParams.gamesSlug);
    });
