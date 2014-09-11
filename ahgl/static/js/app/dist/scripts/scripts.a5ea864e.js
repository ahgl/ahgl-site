"use strict";angular.module("config",[]).constant("ENV",{name:"production",apiEndpoint:""}),angular.module("ahglApp",["config","ngAnimate","ngCookies","ngResource","ngRoute","ngSanitize","ngTouch","angular-carousel"]).config(["$routeProvider",function(a){a.when("/",{templateUrl:"views/main.html",controller:"MainCtrl"}).otherwise({redirectTo:"/"})}]),angular.module("ahglApp").controller("MainCtrl",function(){}),angular.module("ahglApp").controller("HeaderCtrl",["$scope","GamesSvc",function(a,b){b.fetchGames().then(function(b){a.games=b})}]),angular.module("ahglApp").controller("LiveStreamCtrl",["$scope","$sce","liveStreamSvc","urlSvc","GamesSvc",function(a,b,c,d,e){c.fetchStreams().then(function(c){a.liveStream=!0,a.channel_name=c.channelName,a.chat_url=b.trustAsResourceUrl(d.chatUrl.replace("{{channelName}}",c.channelName)),a.live_stream_logo=b.trustAsResourceUrl(c.gameImageUrl),a.streamTitle=c.channelName}),e.fetchGames().then(function(){a.sectionHeaderIconUrl=e.getRandomIcon("live_stream")})}]),angular.module("ahglApp").controller("CarouselCtrl",["$scope","carouselSvc","$sce",function(a,b,c){a.carouselInterval=5e3,a.slides=[],b.fetchCarousels().then(function(b){b.data.results.forEach(function(b){b.message=c.trustAsHtml(b.message),a.slides.push(b)})})}]),angular.module("ahglApp").controller("FeaturedMatchesCtrl",["$scope","$sce","urlSvc","MatchSvc","GamesSvc",function(a,b,c,d,e){a.localGamesSvc=e,d.fetchMatches().then(function(b){a.matches=b}),e.fetchGames().then(function(){a.sectionHeaderIconUrl=e.getRandomIcon("match")})}]),angular.module("ahglApp").controller("LatestNewsCtrl",["$scope","$sce","urlSvc","NewsSvc","GamesSvc",function(a,b,c,d,e){a.localGamesSvc=e,d.fetchNews().then(function(b){a.news=b}),e.fetchGames().then(function(){a.sectionHeaderIconUrl=e.getRandomIcon("article")})}]),angular.module("ahglApp").service("urlSvc",["ENV",function(a){this.carouselUrl=a.apiEndpoint+"/api/carousel/?format=json",this.headerInfoUrl=a.apiEndpoint+"/api/header/?format=json",this.gamesUrl=a.apiEndpoint+"/api/games/?format=json",this.streamUrl="https://api.twitch.tv/kraken/streams/{{channelName}}?callback=JSON_CALLBACK",this.chatUrl="http://twitch.tv/chat/embed?channel={{channelName}}&amp;popout_chat=false",this.matchesUrl=a.apiEndpoint+"/api/featured_matches/?format=json",this.newsUrl=a.apiEndpoint+"/api/latest_news/?format=json"}]),angular.module("ahglApp").service("liveStreamSvc",["$sce","$http","$q","urlSvc",function(a,b,c,d){this.fetchStreams=function(){var a=c.defer();return this.fetchGames().then(function(e){var f=[];e.data.results.forEach(function(a){f.push(b.jsonp(d.streamUrl.replace("{{channelName}}",a.channel_name)))}),c.all(f).then(function(b){b.some(function(b,c){if(b.data.stream){var d=e.data.results[c],f=d.channel_name,g=d.section_image_url;return a.resolve({channelName:f,gameImageUrl:g}),!0}})})}),a.promise},this.fetchGames=function(){return b.get(a.trustAsResourceUrl(d.gamesUrl))}}]),angular.module("ahglApp").service("MatchSvc",["$sce","$http","$q","urlSvc",function(a,b,c,d){this.fetchMatches=function(){return b.get(d.matchesUrl).then(function(a){var b=_.map(a.data.results,function(a){return a});return b.slice(0,3)})}}]),angular.module("ahglApp").service("carouselSvc",["$sce","$http","$q","urlSvc",function(a,b,c,d){this.fetchCarousels=function(){return b.get(d.carouselUrl)}}]),angular.module("ahglApp").service("NewsSvc",["$sce","$http","$q","urlSvc",function(a,b,c,d){this.fetchNews=function(){return b.get(d.newsUrl).then(function(a){return a.data.results})}}]),angular.module("ahglApp").run(["$templateCache",function(a){a.put("views/carousel.html",'<div ng-controller=CarouselCtrl class=carousel-container><ul rn-carousel rn-carousel-control><li ng-repeat="slide in slides"><img ng-src="{{slide.image_url}}"><div class=mask></div><div class=fade></div><div class=message><span ng-bind-html=slide.message></span></div></li></ul></div>'),a.put("views/featuredMatches.html",'<div ng-controller=FeaturedMatchesCtrl><div class=header><img class=section-header-icon ng-src="{{ sectionHeaderIconUrl }}"> <span class=heavy>Featured</span><span>Matches</span></div><div class=featured-matches><div ng-repeat="match in matches" class=match style="background-image: url(\'{{match.background_image_url}}\')"><a href="{{ match.match_url }}"><p>{{ match.home_team }}</p><p class=vs>vs</p><p>{{ match.away_team }}</p></a></div></div></div>'),a.put("views/footer.html",'<div class=bar><ul><li><a href=/ahgl-handbook>HANDBOOK</a> |</li><li><a href=/faq>FAQ</a> |</li><li><a href=/press>PRESS</a> |</li><li><a href=/archive>PAST SEASONS</a> |</li><li><a href=/leadership>LEADERSHIP</a> |</li><li><a href=/messages/compose/ahgltv>CONTACT</a></li></ul></div><div class=social><ul><a href=http://www.facebook.com/AHGLtv><li class=facebook></li></a> <a href=http://twitter.com/ahgltv><li class=twitter></li></a> <a href=http://www.youtube.com/afterhoursgamingtv><li class=youtube></li></a> <a href=http://www.twitch.tv/ahgltv><li class=twitch></li></a></ul></div><div class=misc><div class=terms><div><a href=/terms-of-use>TERMS OF USE</a></div><div>©2014 JINK.TV. ALL RIGHTS RESERVED</div></div><div class=icon></div><div class=built-by><div>SITE BUILT BY <b><a href="http://ntucker.me/">NATHANIEL TUCKER</a></b></div><div>AND DESIGNED BY <b><a href="http://rediceinteractive.com/">REDICE</a></b></div></div></div>'),a.put("views/header.html",'<a href="/"><div class=logo></div></a><div class=bar ng-controller=HeaderCtrl><a ng-repeat="game in games" href="/tournament/{{ game.slug }}"><img class="game1 game" ng-src="{{ game.image_url}}"></a></div><div class=navigation><ul><li>VIDEOS</li><li>CASTERS</li><li>TEAMS</li><li>SCHEDULE</li><li>STANDINGS</li></ul></div>'),a.put("views/latestNews.html",'<div ng-controller=LatestNewsCtrl><div class=header><img class=section-header-icon ng-src="{{ sectionHeaderIconUrl }}"> <span class=heavy>Latest</span><span>Ahgl News</span></div><div class=latest-news><div ng-repeat="article in news" class=news><div class=news-heading><div class=date>Aug 15th, 2014</div><img ng-show=article.image_url src="/{{ article.icon_image_url }}"><div>{{ article.title }}</div><div class=underline></div></div><p ng-bind-html=article.summary></p><a href="{{ article.page_url }}">Read More</a></div></div></div>'),a.put("views/liveStream.html",'<div ng-controller=LiveStreamCtrl class=live-stream ng-show=liveStream><div class=header><img class=section-header-icon ng-src="{{ sectionHeaderIconUrl }}"> <span class=heavy>Live</span><span>stream</span></div><div class=title-container><div class=title>{{streamTitle}}</div><div class=currently-playing>Currently Playing</div></div><div class=stream-container><object type=application/x-shockwave-flash height=500 width=600 id=live_embed_player_flash data="http://www.twitch.tv/widgets/live_embed_player.swf?channel={{channel_name}}" bgcolor=#000000 class=twitch-container><param name=allowFullScreen value="true"><param name=allowScriptAccess value="always"><param name=allowNetworking value="all"><param name=movie value="http://www.twitch.tv/widgets/live_embed_player.swf"><param name=flashvars value="hostname=www.twitch.tv&channel={{channel_name}}&auto_play=true&start_volume=50"></object><iframe class=chat-container frameborder=0 scrolling=no id=chat_embed ng-src={{chat_url}}></iframe></div></div>'),a.put("views/main.html",'<header ng-include="\'views/header.html\'"></header><div class=carousel ng-include="\'views/carousel.html\'"></div><div class="section live-stream" ng-include="\'views/liveStream.html\'"></div><div class=section ng-include="\'views/featuredMatches.html\'"></div><div class=section ng-include="\'views/latestNews.html\'"></div><footer ng-include="\'views/footer.html\'"></footer>')}]);