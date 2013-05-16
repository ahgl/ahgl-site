from social_auth.backends.facebook import FacebookBackend
from account.auth_backends import HybridAuthenticationBackend
from phileo.auth_backends import CanLikeBackend


class FbLikableBackend(CanLikeBackend, FacebookBackend):
    pass


class HybridLikeableBackend(CanLikeBackend, HybridAuthenticationBackend):
    pass
