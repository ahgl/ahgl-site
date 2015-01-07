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
            $scope.sectionHeaderIconUrl = GamesSvc.getIcon("article", selectedGame);
        });

        var monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
        $scope.formatDate = function(article) {
            var date = new Date(article.publish_date);
            if (!date) {
                return "";
            }
            var dateStr = monthNames[date.getMonth()] + " " + date.getDay() + ", " + date.getFullYear()
            return dateStr;
        };

        $scope.isVisible = function(article) {
            return article.icon_image_url !== null;
        };
    });
