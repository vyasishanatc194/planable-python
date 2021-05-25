from rest_framework.views import APIView
from ..serializers import UserProfileImageSerializer
from planable.helpers import custom_response, serialized_response
from rest_framework import status
from planable.permissions import IsAccountOwner
from ..models import User, UserProfileImage
from ..serializers import (
    UserProfileImageSerializer,
    UserProfileSerializer,
    UserProfileUpdateSerializer,
)


class ProfileImageAPIView(APIView):
    """
    User Sign up view
    """

    serializer_class = UserProfileImageSerializer
    permission_classes = (IsAccountOwner,)

    def post(self, request, *args, **kwargs):
        request.data["user"] = request.user.pk
        message = "Profile image added successfully!"
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        response_status, result, message = serialized_response(serializer, message)
        status_code = (
            status.HTTP_200_OK if response_status else status.HTTP_400_BAD_REQUEST
        )
        return custom_response(response_status, status_code, message, result)

    def get(self, request):
        profile_images = UserProfileImage.objects.filter(user=request.user.pk)
        serializer = self.serializer_class(
            profile_images, many=True, context={"request": request}
        )
        message = "User Profile images fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)

    def delete(self, request, pk):
        profile_images = UserProfileImage.objects.filter(pk=pk)
        if not profile_images:
            message = "Image not found!"
            return custom_response(False, status.HTTP_200_OK, message)
        profile_images.delete()
        message = "Image removed successfully!"
        return custom_response(True, status.HTTP_200_OK, message, [])


class UserProfileAPIView(APIView):
    """
    User Sign up view
    """

    serializer_class = UserProfileSerializer
    permission_classes = (IsAccountOwner,)

    def get(self, request):
        user = User.objects.filter(pk=request.user.pk)
        serializer = self.serializer_class(user.first(), context={"request": request})
        message = "User Profile fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)

    def put(self, request, *args, **kwargs):
        user = User.objects.filter(pk=request.user.pk)
        if not user:
            message = "User not found!"
            return custom_response(False, status.HTTP_200_OK, message)
        message = "User Profile updated successfully!"
        serializer = UserProfileUpdateSerializer(
            user.first(), data=request.data, partial=True, context={"request": request}
        )
        response_status, result, message = serialized_response(serializer, message)
        status_code = (
            status.HTTP_200_OK if response_status else status.HTTP_400_BAD_REQUEST
        )
        return custom_response(response_status, status_code, message, result)


class ViewProfileAPIView(APIView):
    """
    User Sign up view
    """

    serializer_class = UserProfileSerializer
    permission_classes = ()

    def get(self, request, pk):
        user = User.objects.filter(pk=pk)
        if not user:
            message = "User not found!!!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
        serializer = self.serializer_class(user.first(), context={"request": request})
        message = "User Profile fetched Successfully!!!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)
