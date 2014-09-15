'use strict';

angular.module('ahglApp')
    .controller('LatestNewsCtrl', function ($scope, $sce, urlSvc, NewsSvc, GamesSvc) {
        $scope.localGamesSvc = GamesSvc;
        $scope.newsPresent = false;

        var selectedGame = GamesSvc.getSelectedGame();

        NewsSvc.fetchNews(selectedGame).then(function(news) {
                $scope.news = news;
                $scope.newsPresent = news.length > 0;
        });

        GamesSvc.fetchGames().then(function(games) {
            $scope.sectionHeaderIconUrl = GamesSvc.getRandomIcon("article");
        });
    });
