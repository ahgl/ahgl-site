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
