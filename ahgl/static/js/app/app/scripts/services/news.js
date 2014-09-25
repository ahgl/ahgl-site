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
                
        this.fetchNews = function (tournamentFilter) {
            var data = {};
            if (tournamentFilter) {
                data.tournament = tournamentFilter;
            }
            return $http.get(urlSvc.newsUrl, {params: data}).then(function(resp) {    
                return resp.data.results;
            });
        };
    });
