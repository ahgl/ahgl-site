'use strict';

/**
 * @ngdoc function
 * @name ahglApp.controller:CarouselCtrl
 * @description
 * # CarouselCtrl
 * Controller of the ahglApp
 */
angular.module('ahglApp')
    .controller('CarouselCtrl', function ($scope, carouselSvc, $sce) {
        $scope.carouselInterval = 5000;
        $scope.slides = [
        	{
        		image: 'http://placekitten.com/605/300',
        		message: $sce.trustAsHtml('<b>hi</b><br/>there')
        	},
        	{
        		image: 'http://placekitten.com/601/300'
        	}
        ]
    });