import requests
from django.conf import settings
from rest_framework.views import APIView
from ..serializers import UserRegisterSerializer, CityListingSerializer
from planable.helpers import custom_response, serialized_response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from planable.permissions import IsAccountOwner
from ..models import User, City
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from instagram_basic_display.InstagramBasicDisplay import InstagramBasicDisplay


class SignUpApiView(APIView):
    """
    User Sign up view
    """

    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        if "email" in request.data:
            email_check = User.objects.filter(email=request.data["email"]).distinct()
            if email_check.exists():
                message = "Email already exists!"
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
            message = "Account created successfully!"
            serializer = UserRegisterSerializer(
                data=request.data, context={"request": request}
            )
            response_status, result, message = serialized_response(serializer, message)
            status_code = (
                status.HTTP_201_CREATED
                if response_status
                else status.HTTP_400_BAD_REQUEST
            )
            # TODO Email
            return custom_response(response_status, status_code, message, result)
        else:
            return custom_response(
                False, status.HTTP_400_BAD_REQUEST, "Email is required"
            )


class CityListingAPIView(APIView):
    """
    Class Search API
    """

    serializer_class = CityListingSerializer
    permission_classes = ()

    def get(self, request):
        cities = City.objects.filter(active=True)
        serializer = self.serializer_class(
            cities, many=True, context={"request": request}
        )
        message = "Cities fetched successfully!!!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)


class LoginAPIView(APIView):
    """
    User Login View
    """

    serializer_class = UserRegisterSerializer

    def post(self, request, format=None):
        email = request.data.get("email", None)
        password = request.data.get("password", None)
        account = authenticate(email=email, password=password)

        if account is not None:
            login(request, account)
            serializer = self.serializer_class(account, context={"request": request})
            return custom_response(
                True, status.HTTP_200_OK, "Login Successful!", serializer.data
            )
        else:
            message = "Email/password combination invalid"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)


class LogoutAPIView(APIView):
    """
    User Logout View
    """

    permission_classes = (IsAccountOwner,)

    def post(self, request, format=None):
        request.user.auth_token.delete()
        logout(request)
        message = "Logout successful!"
        return custom_response(True, status.HTTP_200_OK, message)


class SaveInstagramTokenAPI(APIView):

    permission_classes = (IsAccountOwner,)

    def post(self, request, format=None):
        """
        POST method to create the data
        """       
        code  = request.data.get("code", None)
        if not code:
            message = "Instagram tokens required!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
        user = User.objects.get(pk=request.user.pk)
        user.instagram_code = code
        user.save()
        message = "Connected to Instagram successfully!"
        return custom_response(True, status.HTTP_200_OK, message)


class DisconnectInstagramAPI(APIView):

    permission_classes = (IsAccountOwner,)

    def post(self, request, format=None):
        """
        POST method to create the data
        """       
        user = User.objects.get(pk=request.user.pk)
        user.instagram_code = None
        user.save()
        message = "Disconnected from Instagram successfully!"
        return custom_response(False, status.HTTP_200_OK, message)


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

    def get_response(self):
        serializer_class = self.get_response_serializer()
        data = {
            'user': self.user,
            'key': self.token
        }
        serializer = serializer_class(instance=data, context={'request': self.request})
        response_status = True
        status_code = status.HTTP_200_OK
        message = "Login Successful!"
        result = serializer.data
        result_data = {'token': "Token " + result['key'], 'user': str(self.user.id)}
        return custom_response(response_status, status_code, message, result_data)


class InstagramAPIView(APIView):
    """
    Class Instagram API
    """

    permission_classes = (IsAccountOwner,)

    def post(self, request, format=None):
        """
        POST method to create the data
        """
        try:
            instagram_basic_display = InstagramBasicDisplay(
                app_id=settings.INSTAGRAM_APP_ID,
                app_secret=settings.INSTAGRAM_APP_SECRET,
                redirect_url=settings.INSTAGRAM_REDIRECT_URL
            )
            code = request.data.get("code", None)
            if not code:
                message = "Instagram token is required!"
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
            short_lived_token = instagram_basic_display.get_o_auth_token(code)
            long_lived_token = instagram_basic_display.get_long_lived_token(short_lived_token.get('access_token'))
            instagram_basic_display.set_access_token(long_lived_token.access_token)
            user = User.objects.get(pk=request.user.pk)
            user.instagram_code = long_lived_token.access_token
            user.save()
            message = "Connected to Instagram successfully!"
            data = {"access_token": long_lived_token.access_token}
            return custom_response(True, status.HTTP_200_OK, message, data)
        except Exception as inst:
            return custom_response(False, status.HTTP_400_BAD_REQUEST, str(inst))


class ConnectInstagramAPI(APIView):
    """
    Class Instagram API
    """

    permission_classes = (IsAccountOwner,)

    def post(self, request, format=None):
        """
        POST method to create the data
        """
        try:
            code = request.data.get("code", None)
            if not code:
                message = "Instagram token is required!"
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
            url_short = settings.INSTAGRAM_SHORT_ACCESS_TOKEN_URL
            payload_short = {
                'client_id': settings.INSTAGRAM_APP_ID,
                'client_secret': settings.INSTAGRAM_APP_SECRET,
                'grant_type': 'authorization_code',
                'redirect_uri': settings.INSTAGRAM_REDIRECT_URL,
                'code': code,
            }
            files_short = []
            headers_short = {
                'Cookie': request.headers['Cookie']
            }
            response_short = requests.request("POST", url_short, headers=headers_short,
                                              data=payload_short, files=files_short)
            data_short = response_short.json()

            if response_short.status_code == 200:
                url_long = settings.INSTAGRAM_LONG_ACCESS_TOKEN_URL + \
                        "?grant_type=ig_exchange_token" \
                        "&client_secret=" + settings.INSTAGRAM_APP_SECRET + \
                        "&access_token=" + data_short['access_token']

                payload_long = {}
                headers_long = {
                    'Cookie': request.headers['Cookie']
                }
                response_long = requests.request("GET", url_long, headers=headers_long,
                                                 data=payload_long)
                data_long = response_long.json()
                if response_long.status_code == 200:
                    url_media = settings.INSTAGRAM_USER_MEDIA_URL + \
                          "?fields=media_type,media_url,thumbnail_url" \
                          "&access_token=" + data_long['access_token']
                    payload_media = {}
                    headers_media = {
                        'Cookie': request.headers['Cookie']
                    }
                    response_media = requests.request("GET", url_media, headers=headers_media,
                                                      data=payload_media)
                    data_media = response_media.json()
                    post_list = data_media['data']
                    final_list = []
                    for i in post_list:
                        if i['media_type'] == 'CAROUSEL_ALBUM':
                            pass
                        elif i['media_type'] == 'VIDEO':
                            final_list.append(i['thumbnail_url'])
                        else:
                            final_list.append(i['media_url'])
                    data_long["instagram_posts"] = final_list

                    user = User.objects.get(pk=request.user.pk)
                    user.instagram_code = data_long['access_token']
                    user.save()
                    message = "Connected to Instagram successfully!"
                    return custom_response(True, status.HTTP_200_OK, message, data_long)
                else:
                    message = "Something went wrong!"
                    return custom_response(False, response_long.status_code, message, data_long)
            else:
                message = "Something went wrong!"
                return custom_response(False, response_short.status_code, message, data_short)
        except Exception as inst:
            return custom_response(False, status.HTTP_400_BAD_REQUEST, str(inst))
