import re
from rest_framework.views import APIView
from rest_framework import permissions, status, generics
from rest_framework.response import Response
from django.contrib import auth
from django.contrib.auth.models import User
from user_profile.models import Profile
from .serializers import UsersSerializers
from django.http import Http404

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect


@method_decorator(ensure_csrf_cookie, name="dispatch")
class GetCSRFView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        return Response({"Success": "CSRF cookie set!"}, status=status.HTTP_200_OK)


@method_decorator(csrf_protect, name="dispatch")
class CheckAuthenticatedView(APIView):
    def get(self, request, format=None):
        try:
            user = request.user
            IsAuthenticated = user.is_authenticated
            if IsAuthenticated:
                return Response(
                    {"Success": f"{user.username} is authenticated!"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"Unauthorized": "No authentication credentials provided"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except Exception as e:
            return Response(
                {"Error": f"Something went wrong!: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@method_decorator(csrf_protect, name="dispatch")
class SignUpView(APIView):
    permission_classes = [permissions.AllowAny]

    def get_user(self):
        try:
            return User.objects.get(username=self.request.data["username"])
        except User.DoesNotExist():
            raise Http404("User does not exist!")

    def post(self, request, format=None):
        data = request.data
        username = data["username"]
        password = data["password"]
        re_password = data["re_password"]
        password_regex = (
            r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        )

        if password != re_password:
            return Response(
                {"Error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST
            )
        if User.objects.filter(username=username).exists():
            return Response(
                {"Error": "Username already exists!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(password) < 8:
            return Response(
                {"Error": "Password must be at least 8 characters"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not re.match(password_regex, password):
            return Response(
                {
                    "Error": "Password must have at least one uppercase letter, one lower case letter, one special character and contain at least 8 characters!"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:

            user = User.objects.create_user(username=username, password=password)
            user.save()

            user_instance = self.get_user()
            user_profile = Profile.objects.create(user=user_instance)
            user_profile.save()
            return Response(
                {"Success": "User created successfully!"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"Error": f"Sign up failed!: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@method_decorator(csrf_protect, name="dispatch")
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        data = request.data
        username = data["username"]
        password = data["password"]

        if not username or not password:
            return Response(
                {"Error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = auth.authenticate(username=username, password=password)
            if user is not None:

                auth.login(request, user)
                return Response(
                    {"Success": f"User {username} logged in successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"Error": f"{username} is None"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except Exception as e:
            return Response(
                {"Error": f"Something went wrong: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LogoutView(APIView):
    def post(self, request, format=None):
        try:
            auth.logout(request)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(
                {"Error": f"Logout failed due to: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DeleteUserView(APIView):
    def delete(self, request, format=None):
        try:
            User.objects.filter(id=request.user.id).delete()
            return Response(
                {"Success": f"{request.user.username} deleted successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"Error": f"Action failed! {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ListUsersView(generics.ListAPIView):
    serializer_class = UsersSerializers
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]
