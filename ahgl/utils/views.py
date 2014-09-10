import os

from django.conf import settings
from django.http import HttpResponse
from django.views.generic.base import View

class ObjectPermissionsCheckMixin(object):
    def check_permissions(self):
        """Override this to check permissions."""
        pass

    def dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(),
                              self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.object = self.get_object()
        self.get_object = lambda: self.object
        return self.check_permissions() or handler(request, *args, **kwargs)

# Simple view to serve a static file from the project root. Used to serve the
# new Angular app.
#
# TODO: In production, do something smarter, like use X-Sendfile.
# See http://stackoverflow.com/questions/2294507
class StaticFileView(View):

    path = None

    def get(self, request, *args, **kwargs):
        if self.path is None:
            raise Exception("StaticFileView path attribute must be defined.")
        abspath = os.path.join(settings.PROJECT_ROOT, self.path)
        try:
            fh = open(abspath, 'r')
            contents = fh.read()
        except Exception as e:
            raise Exception("StaticFileView could not read file at %s: %s" % (self.path, e))
        return HttpResponse(contents)
