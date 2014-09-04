'use strict';

/**
 * @ngdoc function
 * @name ahglApp.services:carouselSvc
 * @description
 * # carouselSvc
 * Controller of the ahglApp
 */
angular.module('ahglApp')
    .service('carouselSvc', function ($sce, $http, $q, urlSvc) {
        
        this.fetchCarousels = function () {
            return $http.get(urlSvc.carouselUrl);
        }
    });
