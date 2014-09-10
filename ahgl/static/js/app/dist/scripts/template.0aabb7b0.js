angular.module('ahglApp').run(['$templateCache', function($templateCache) {
  'use strict';

  $templateCache.put('views/carousel.html',
    "<div ng-controller=CarouselCtrl class=carousel-container><ul rn-carousel rn-carousel-control><li ng-repeat=\"slide in slides\"><img ng-src=\"{{slide.image_url}}\"><div class=mask></div><div class=fade></div><div class=message><span ng-bind-html=slide.message></span></div></li></ul></div>"
  );


  $templateCache.put('views/footer.html',
    "<div class=bar><ul><li>HANDBOOK |</li><li>FAQ |</li><li>PRESS |</li><li>PAST SEASONS |</li><li>LEADERSHIP |</li><li>CONTACT</li></ul></div><div class=social><ul><li class=facebook></li><li class=twitter></li><li class=youtube></li><li class=twitch></li></ul></div><div class=misc><div class=terms><div>TERMS OF USE</div><div>©2014 JINK.TV. ALL RIGHTS RESERVED</div></div><div class=icon></div><div class=built-by><div>SITE BUILT BY <b>NATHANIEL TUCKER</b></div><div>AND DESIGNED BY <b>REDICE</b></div></div></div>"
  );


  $templateCache.put('views/header.html',
    "<div class=logo></div><div class=bar ng-controller=HeaderCtrl><span ng-repeat=\"url in gameImages\"><img class=\"game1 game\" ng-src=\"{{url}}\"></span></div><div class=navigation><ul><li>VIDEOS</li><li>CASTERS</li><li>TEAMS</li><li>SCHEDULE</li><li>STANDINGS</li></ul></div>"
  );


  $templateCache.put('views/liveStream.html',
    "<div ng-controller=LiveStreamCtrl class=livestream-container ng-show=liveStream><div class=header></div><div class=title-container><img class=logo ng-src=\"{{live_stream_logo}}\"><div class=title>{{streamTitle}}</div><div class=currently-playing>Currently Playing</div></div><div class=stream-container><object type=application/x-shockwave-flash height=500 width=600 id=live_embed_player_flash data=\"http://www.twitch.tv/widgets/live_embed_player.swf?channel={{channel_name}}\" bgcolor=#000000 class=twitch-container><param name=allowFullScreen value=\"true\"><param name=allowScriptAccess value=\"always\"><param name=allowNetworking value=\"all\"><param name=movie value=\"http://www.twitch.tv/widgets/live_embed_player.swf\"><param name=flashvars value=\"hostname=www.twitch.tv&channel={{channel_name}}&auto_play=true&start_volume=50\"></object><iframe class=chat-container frameborder=0 scrolling=no id=chat_embed ng-src={{chat_url}}></iframe></div></div>"
  );


  $templateCache.put('views/main.html',
    "<header ng-include=\"'views/header.html'\"></header><div class=carousel ng-include=\"'views/carousel.html'\"></div><div class=live-stream ng-include=\"'views/liveStream.html'\"></div><div class=featured-matches></div><div class=latest-news></div><footer ng-include=\"'views/footer.html'\"></footer>"
  );

}]);
