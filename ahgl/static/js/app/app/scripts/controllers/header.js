'use strict';

/**
 * @ngdoc function
 * @name ahglApp.controller:HeaderCtrl
 * @description
 * # HeaderCtrl
 * Controller of the ahglApp
 */
angular.module('ahglApp')
    .controller('HeaderCtrl', function ($scope, headerSvc) {
        headerSvc.fetchHeaderInfo()
            .then(function(resp) {    
                $scope.game1ImageSrc = resp.data.results[0].image_url;
                $scope.game2ImageSrc = resp.data.results[1].image_url;
                $scope.game3ImageSrc = resp.data.results[2].image_url;
                $scope.game4ImageSrc = resp.data.results[3].image_url;
                $scope.game5ImageSrc = resp.data.results[4].image_url;
            });
    });
