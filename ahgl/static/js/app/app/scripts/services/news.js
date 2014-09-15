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
                
        this.fetchNews = function (gameFilter) {
            var data = {};
            if (gameFilter) {
                data.game = gameFilter;
            }
            return $http.get(urlSvc.newsUrl, {params: data}).then(function(resp) {    
                return resp.data.results;
            });
        };
    });
