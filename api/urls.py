from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, EmailAuthenticatedSet,
                    GenreViewSet, ReviewViewSet, TitleViewSet, UsersViewSet)

router_v1 = DefaultRouter()
router_v1.register('auth', EmailAuthenticatedSet, basename='auth_email')
router_v1.register('users', UsersViewSet)
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('titles', TitleViewSet)
router_v1.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
