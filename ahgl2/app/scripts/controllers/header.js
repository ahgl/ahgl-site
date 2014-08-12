'use strict';

/**
 * @ngdoc function
 * @name ahgl2App.controller:HeaderCtrl
 * @description
 * # HeaderCtrl
 * Controller of the ahgl2App
 */
angular.module('ahgl2App')
	.controller('HeaderCtrl', function ($scope) {
		$scope.game1ImageSrc = 'images/game1.png';
		$scope.game2ImageSrc = 'images/game2.png';
		$scope.game3ImageSrc = 'images/game3.png';
		$scope.game4ImageSrc = 'images/game4.png';
	});
