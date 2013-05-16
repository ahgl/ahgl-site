from django.contrib.redirects.models import Redirect
from django import http
from django.conf import settings
from django.core.cache import cache


class RedirectFallbackMiddleware(object):
    def __init__(self):
        self.cache_timeout = getattr(settings, 'CACHE_REDIRECT_SECONDS', 300)
        self.key_prefix = getattr(settings, 'CACHE_REDIRECT_KEY_PREFIX', 'redirect')

    def process_response(self, request, response):
        if response.status_code != 404:
            return response  # No need to check for a redirect for non-404 responses.
        path = request.get_full_path()
        cache_key = " ".join((self.key_prefix, path))
        new_path = cache.get(cache_key, None)
        if new_path is None:
            try:
                r = Redirect.objects.get(site__id__exact=settings.SITE_ID, old_path=path)
            except Redirect.DoesNotExist:
                r = None
            if r is None and settings.APPEND_SLASH:
                # Try removing the trailing slash.
                try:
                    r = Redirect.objects.get(site__id__exact=settings.SITE_ID,
                                             old_path=path[:path.rfind('/')] + path[path.rfind('/') + 1:])
                except Redirect.DoesNotExist:
                    pass
            if r is not None:
                new_path = r.new_path
                cache.set(cache_key, new_path, self.cache_timeout)
        if new_path is not None:
            if new_path == '':
                return http.HttpResponseGone()
            return http.HttpResponsePermanentRedirect(new_path)

        # No redirect was found. Return the response.
        return response
