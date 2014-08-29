'use strict';

/**
 * @ngdoc function
 * @name ahglApp.controller:HeaderCtrl
 * @description
 * # HeaderCtrl
 * Controller of the ahglApp
 */
angular.module('ahglApp')
    .controller('HeaderCtrl', function ($scope, $http) {
        $http.get('http://127.0.0.1:8000/api/header/?format=json').then(function(resp) {    
            $scope.game1ImageSrc = resp.data.results[0].image_url;
            $scope.game2ImageSrc = resp.data.results[1].image_url;
            $scope.game3ImageSrc = resp.data.results[2].image_url;
            $scope.game4ImageSrc = resp.data.results[3].image_url;
            $scope.game5ImageSrc = resp.data.results[4].image_url;
        });
    });
