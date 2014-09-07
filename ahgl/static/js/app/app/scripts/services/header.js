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
            return $http.get(urlSvc.headerInfoUrl).then(function(resp) {    
                var games =  _.map(resp.data.results, function(el) {
                    return {slug: el.game_slug ,image_url: el.image_url};
                });
                return games;
            });
        }  
    });
