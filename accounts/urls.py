from django.urls import path
from .views import (
    GetCSRFView,
    SignUpView,
    LoginView,
    LogoutView,
    CheckAuthenticatedView,
    DeleteUserView,
    ListUsersView,
)

urlpatterns = [
    path("register", SignUpView.as_view()),
    path("csrf_cookie", GetCSRFView.as_view()),
    path("login", LoginView.as_view()),
    path("logout", LogoutView.as_view()),
    path("check_authenticated", CheckAuthenticatedView.as_view()),
    path("delete", DeleteUserView.as_view()),
    path("list_users", ListUsersView.as_view()),
]
