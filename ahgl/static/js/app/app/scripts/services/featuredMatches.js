'use strict';

/**
 * @ngdoc function
 * @name ahglApp.services:MatchSvc
 * @description
 * # MatchSvc
 * Controller of the ahglApp
 */
angular.module('ahglApp')
    .service('MatchSvc', function ($sce, $http, $q, urlSvc) {
                
        this.fetchMatches = function () {
            return $http.get(urlSvc.matchesUrl).then(function(resp) {    
                var matches =  _.map(resp.data.results, function(el) {
                    return el;
                });
                return matches.slice(0,3);
            });
        };
    });
