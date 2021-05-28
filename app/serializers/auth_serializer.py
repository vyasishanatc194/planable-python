import requests
from django.conf import settings
from rest_framework import fields, serializers
from ..models import User, City, UserProfileImage
from rest_framework.authtoken.models import Token


class CityListingSerializer(serializers.ModelSerializer):
    """
    City serializer
    """

    class Meta:
        model = City
        fields = ["id", "city"]


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    User Profile serializer
    """

    email = serializers.EmailField()
    token = serializers.SerializerMethodField(read_only=True)
    password = serializers.CharField(write_only=True, required=False)
    full_name = serializers.CharField(required=True)
    city = serializers.CharField(required=True)
    date_of_birth = serializers.CharField(required=True)
    single_profile_image = serializers.SerializerMethodField("get_single_profile_image")
    profile_images = serializers.SerializerMethodField()
    instagram_posts = serializers.SerializerMethodField("get_instagram_posts")

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "full_name",
            "token",
            "instagram_code",
            "password",
            "city",
            "date_of_birth",
            "single_profile_image",
            "profile_images",
            "instagram_posts",
        ]

        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """
        custom 'create' so that password gets hashed!
        """
        password = validated_data.pop("password", None)
        city = validated_data.pop("city", None)
        check_city = City.objects.filter(pk=city)
        if not check_city:
            return "invalid city selected"

        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.city = check_city.first()
        instance.save()
        return instance

    def get_token(self, obj):
        return f"Token {Token.objects.get_or_create(user=obj)[0]}"

    def get_single_profile_image(self, obj):
        request = self.context.get('request')
        images = UserProfileImage.objects.filter(user=obj.pk)
        if images.exists():
            image = images.first()
            return request.build_absolute_uri(image.profile_image.url)
        return ""

    def get_profile_images(self, instance):
        # TODO: Facing circular import issue in the top level import.
        from ..serializers import UserProfileImageSerializer
        images = UserProfileImage.objects.filter(user=instance.pk)
        image_serializer = UserProfileImageSerializer(
            images, many=True, context={"request": self.context["request"]}
        )
        return image_serializer.data

    def get_instagram_posts(self, instance):
        try:
            request = self.context.get('request')
            access_token = instance.instagram_code

            url = settings.INSTAGRAM_USER_MEDIA_URL + \
                "?fields=media_type,media_url,thumbnail_url" \
                "&access_token=" + access_token
            payload = {}
            headers = {
                'Cookie': request.headers['Cookie']
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            data = response.json()
            post_list = data['data']
            final_list = []
            for i in post_list:
                if i['media_type'] == 'CAROUSEL_ALBUM':
                    pass
                elif i['media_type'] == 'VIDEO':
                    final_list.append(i['thumbnail_url'])
                else:
                    final_list.append(i['media_url'])
            return final_list
        except Exception as inst:
            print(inst)
            return []


class UserViewSerializer(serializers.ModelSerializer):
    """
    User View serializer
    """

    class Meta:
        model = User
        fields = ["id", "email", "full_name"]
