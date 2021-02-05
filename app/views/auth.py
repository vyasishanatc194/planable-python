from rest_framework.views import APIView
from ..serializers import UserRegisterSerializer, CityListingSerializer
from planable.helpers import custom_response, serialized_response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from planable.permissions import IsAccountOwner
from ..models import User, City


class SignUpApiView(APIView):
    """
    User Sign up view
    """
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        if 'email' in request.data:
            email_check = User.objects.filter(email=request.data['email']).distinct()
            if email_check.exists():
                message = "Email already exists!"
                return custom_response(True, status.HTTP_400_BAD_REQUEST, message)
            message = "Account created successfully!"
            serializer = UserRegisterSerializer(data=request.data, context={'request': request})
            response_status, result, message = serialized_response(serializer, message)
            status_code = status.HTTP_201_CREATED if response_status else status.HTTP_400_BAD_REQUEST
            # TODO Email
            return custom_response(response_status, status_code, message, result)
        else:
            return custom_response(False, status.HTTP_400_BAD_REQUEST, "Email is required")



class CityListingAPIView(APIView):
    """
    Class Search API
    """
    serializer_class = CityListingSerializer
    permission_classes = ()

    def get(self, request):
        cities = City.objects.filter(active=True)
        serializer = self.serializer_class(cities, many=True, context={"request": request})
        message = "Cities fetched successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)


class LoginAPIView(APIView):
    """
    User Login View
    """
    def post(self, request, format=None):
        email_or_username = request.data.get("email_or_username", None)
        password = request.data.get("password", None)

        account = authenticate(email=email_or_username, password=password)
        if not account:
            user = User.objects.filter(username=email_or_username)
            if user:
                account = authenticate(email=user[0].email, password=password)
        
        if account is not None:
            login(request, account)
            serializer = UserProfileSerializer(account, context={'request':request})
            return custom_response(True, status.HTTP_200_OK, "Login Successful!", serializer.data)
        else:
            message = "Email/password combination invalid"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
