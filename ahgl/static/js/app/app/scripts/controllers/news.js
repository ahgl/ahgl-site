'use strict';

angular.module('ahglApp')
    .controller('LatestNewsCtrl', function ($scope, $sce, urlSvc, NewsSvc) {
        NewsSvc.fetchNews().then(function(news) {
                $scope.news = news;
            });
    });
