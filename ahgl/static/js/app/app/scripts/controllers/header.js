'use strict';

/**
 * @ngdoc function
 * @name ahglApp.controller:HeaderCtrl
 * @description
 * # HeaderCtrl
 * Controller of the ahglApp
 */
angular.module('ahglApp')
    .controller('HeaderCtrl', function ($scope, GamesSvc) {
        GamesSvc.fetchGames().then(function(games) {
            $scope.games = games;
        });
    });
