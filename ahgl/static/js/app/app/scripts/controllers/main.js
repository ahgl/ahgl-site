'use strict';

/**
 * @ngdoc function
 * @name ahglApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the ahglApp
 */
angular.module('ahglApp')
    .controller('MainCtrl', function (GamesSvc) {
        GamesSvc.selectGameSlug(null);
    });
