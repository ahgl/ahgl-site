'use strict';

angular.module('ahglApp')
    .controller('LatestNewsCtrl', function ($scope, $sce, urlSvc, NewsSvc, GamesSvc) {
        $scope.localGamesSvc = GamesSvc;

        NewsSvc.fetchNews().then(function(news) {
                $scope.news = news;
        });

        GamesSvc.fetchGames().then(function(games) {
            $scope.sectionHeaderIconUrl = GamesSvc.getRandomIcon("article");
        });
    });
