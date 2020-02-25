from django.urls import path
from django.conf.urls import include

from rest_framework.routers import DefaultRouter

from apps.account.views import LoonUserView, LoonRoleView, LoonDeptView, LoonAppTokenView, LoonAppTokenDetailView, \
    LoonLoginView, LoonLogoutView, LoonUserRoleView, LoonRoleUserView, CreateUserViewSet

router = DefaultRouter()

router.register(r'create-user', CreateUserViewSet, basename="create-user")

urlpatterns = [
    path(r'/mcenter-dev/', include(router.urls)),
    path('/users', LoonUserView.as_view()),
    path('/users/<int:user_id>/roles', LoonUserRoleView.as_view()),
    path('/roles', LoonRoleView.as_view()),
    path('/roles/<int:role_id>/users', LoonRoleUserView.as_view()),
    path('/depts', LoonDeptView.as_view()),
    path('/login', LoonLoginView.as_view()),
    path('/logout', LoonLogoutView.as_view()),
    path('/app_token', LoonAppTokenView.as_view()),
    path('/app_token/<int:app_token_id>', LoonAppTokenDetailView.as_view()),
]
