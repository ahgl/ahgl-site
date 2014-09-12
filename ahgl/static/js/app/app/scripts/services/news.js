'use strict';

/**
 * @ngdoc function
 * @name ahglApp.services:MatchSvc
 * @description
 * # NewsSvc
 * Controller of the ahglApp
 */
angular.module('ahglApp')
    .service('NewsSvc', function ($sce, $http, $q, urlSvc) {
                
        this.fetchNews = function () {
            return $http.get(urlSvc.newsUrl).then(function(resp) {    
                return resp.data.results;
            });
        };
    });
