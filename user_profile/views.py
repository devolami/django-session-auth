from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializers
from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404

class ProfileView(APIView):
    def get(self, request, format=None):
        try:
            user_id = request.user.id
            username = request.user.username
            user = User.objects.get(id=user_id)
            user_profile = Profile.objects.get(user=user)
            user_profile = ProfileSerializers(user_profile)
            return Response(
                {"profile": user_profile.data, "username": str(username)},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(f"{str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProfileUpdateView(APIView):

    def patch(self, request, format=None):
        data = request.data
        user = request.user

        update_fields = {}

        fields = ["first_name", "last_name", "city", "phone_number", "age"]

        for field in fields:
            if field in data and data[field]:
                if field == "age":
                    try:
                        update_fields["age"] = int(data["age"])
                    except ValueError:
                        return Response({"Error": "Age must be a valid integer."}, status=status.HTTP_400_BAD_REQUEST)

                else:
                    update_fields[field] = data[field]
        user_profile = get_object_or_404(Profile, user=user)
        try:
            for field, value in update_fields.items():
                setattr(user_profile, field, value)
                user_profile.save()
            serialized_profile = ProfileSerializers(user_profile)
            return Response(
                {"profile": serialized_profile.data, "username": user.username},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"Error": f"Something went wrong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ProfileUpdateTwoView(APIView):

    def patch(self, request, format=None):
        data = request.data
        user = request.user

        update_fields = {}

        fields = ["first_name", "last_name", "city", "phone_number", "age"]

        for field in fields:
            if field in data and data[field]:
                if field == "age":
                    try:
                        update_fields["age"] = int(data["age"])
                    except ValueError:
                        return Response({"Error": "Age must be a valid integer."}, status=status.HTTP_400_BAD_REQUEST)

                else:
                    update_fields[field] = data[field]
        user_profile = get_object_or_404(Profile, user=user)
        try:
            for field, value in update_fields.items():
                setattr(user_profile, field, value)
            serialized_profile = ProfileSerializers(user_profile)
            serialized_profile.is_valid(raise_exception=True)
            serialized_profile.save()
            return Response(
                {"profile": serialized_profile.data, "username": user.username},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"Error": f"Something went wrong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)