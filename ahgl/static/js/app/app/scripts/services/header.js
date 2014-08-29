'use strict';

/**
 * @ngdoc function
 * @name ahglApp.services:headerSvc
 * @description
 * # headerSvc
 * Controller of the ahglApp
 */
angular.module('ahglApp')
    .service('headerSvc', function ($sce, $http, urlSvc) {
        
        this.fetchHeaderInfo = function () {
            return $http.get(urlSvc.headerInfoUrl);
        }  
    });
