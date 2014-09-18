angular.module('ahglApp').run(['$templateCache', function($templateCache) {
  'use strict';

  $templateCache.put('views/carousel.html',
    "<div ng-controller=CarouselCtrl class=carousel-container><ul rn-carousel rn-carousel-control><li ng-repeat=\"slide in slides\"><img ng-src=\"{{slide.image_url}}\"><div class=mask></div><div class=fade></div><div class=message><span ng-bind-html=slide.message></span></div></li></ul></div>"
  );


  $templateCache.put('views/featuredMatches.html',
    "<div ng-controller=FeaturedMatchesCtrl ng-show=featuredMatchesPresent><div class=header><img class=section-header-icon ng-src=\"{{ sectionHeaderIconUrl }}\"> <span class=heavy>Featured</span><span>Matches</span></div><div class=featured-matches><div ng-repeat=\"match in matches\" class=match style=\"background-image: url( {{ match.background_image_url }} )\"><a href=\"{{ match.match_url }}\"><p>{{ match.home_team }}</p><p class=vs>vs</p><p>{{ match.away_team }}</p></a></div></div></div>"
  );


  $templateCache.put('views/footer.html',
    "<div class=bar><ul><li><a href=/ahgl-handbook>HANDBOOK</a> |</li><li><a href=/faq>FAQ</a> |</li><li><a href=/press>PRESS</a> |</li><li><a href=/archive>PAST SEASONS</a> |</li><li><a href=/leadership>LEADERSHIP</a> |</li><li><a href=/messages/compose/ahgltv>CONTACT</a></li></ul></div><div class=social><ul><a href=http://www.facebook.com/AHGLtv><li class=facebook></li></a> <a href=http://twitter.com/ahgltv><li class=twitter></li></a> <a href=http://www.youtube.com/afterhoursgamingtv><li class=youtube></li></a> <a href=http://www.twitch.tv/ahgltv><li class=twitch></li></a></ul></div><div class=misc><div class=terms><div><a href=/terms-of-use>TERMS OF USE</a></div><div>©2014 JINK.TV. ALL RIGHTS RESERVED</div></div><div class=icon></div><div class=built-by><div>SITE BUILT BY <b><a href=\"http://ntucker.me/\">NATHANIEL TUCKER</a></b></div><div>AND DESIGNED BY <b><a href=\"http://rediceinteractive.com/\">REDICE</a></b></div></div></div>"
  );


  $templateCache.put('views/header.html',
    "<a href=\"/\"><div class=logo></div></a><div class=bar ng-controller=HeaderCtrl><a ng-repeat=\"game in games\" href=\"/#/game/{{ game.slug }}\"><img class=\"game1 game\" ng-src=\"{{ getImageUrl(game) }}\"></a></div><div class=navigation ng-show=isGameSelected><ul><li>VIDEOS</li><li>CASTERS</li><li>TEAMS</li><li>SCHEDULE</li><li>STANDINGS</li></ul></div>"
  );


  $templateCache.put('views/latestNews.html',
    "<div ng-controller=LatestNewsCtrl ng-show=newsPresent><div class=header><img class=section-header-icon ng-src=\"{{ sectionHeaderIconUrl }}\"> <span class=heavy>Latest</span><span>Ahgl News</span></div><div class=latest-news><div ng-repeat=\"article in news\" class=news><div class=news-heading><div class=date>Aug 15th, 2014</div><img ng-show=article.image_url ng-src=\"/{{ article.icon_image_url }}\"><div>{{ article.title }}</div><div class=underline></div></div><p ng-bind-html=article.summary></p><a href=\"{{ article.page_url }}\">Read More</a></div></div></div>"
  );


  $templateCache.put('views/liveStream.html',
    "<div ng-controller=LiveStreamCtrl class=live-stream ng-show=liveStream><div class=header><img class=section-header-icon ng-src=\"{{ sectionHeaderIconUrl }}\"> <span class=heavy>Live</span><span>stream</span></div><div class=title-container><div class=title>{{streamTitle}}</div><div class=currently-playing>{{ username }} playing {{ gameName }}</div></div><div class=stream-container><object type=application/x-shockwave-flash height=500 width=600 id=live_embed_player_flash data=\"http://www.twitch.tv/widgets/live_embed_player.swf?channel={{channel_name}}\" bgcolor=#000000 class=twitch-container><param name=allowFullScreen value=\"true\"><param name=allowScriptAccess value=\"always\"><param name=allowNetworking value=\"all\"><param name=movie value=\"http://www.twitch.tv/widgets/live_embed_player.swf\"><param name=flashvars value=\"hostname=www.twitch.tv&channel={{channel_name}}&auto_play=true&start_volume=50\"></object><iframe class=chat-container frameborder=0 scrolling=no id=chat_embed ng-src={{chat_url}}></iframe></div></div>"
  );


  $templateCache.put('views/main.html',
    "<header ng-include=\"'views/header.html'\"></header><div class=carousel ng-include=\"'views/carousel.html'\"></div><div class=\"section live-stream\" ng-include=\"'views/liveStream.html'\"></div><div class=section ng-include=\"'views/featuredMatches.html'\"></div><div class=section ng-include=\"'views/latestNews.html'\"></div><footer ng-include=\"'views/footer.html'\"></footer>"
  );

}]);
