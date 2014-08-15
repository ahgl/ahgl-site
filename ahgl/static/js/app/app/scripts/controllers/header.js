'use strict';

/**
 * @ngdoc function
 * @name ahgl2App.controller:HeaderCtrl
 * @description
 * # HeaderCtrl
 * Controller of the ahgl2App
 */
angular.module('ahgl2App')
    .controller('HeaderCtrl', function ($scope, $http) {
        $http.get('http://127.0.0.1:8000/api/header/?format=json').then(function(resp) {    
            $scope.game1ImageSrc = resp.data.results[0].image_url;
            $scope.game2ImageSrc = resp.data.results[1].image_url;
            $scope.game3ImageSrc = resp.data.results[2].image_url;
            $scope.game4ImageSrc = resp.data.results[3].image_url;
        });
    });
