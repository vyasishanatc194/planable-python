import requests
from django.conf import settings
from rest_framework import fields, serializers
from ..models import UserProfileImage, User, City, PlanJoiningRequest, Plan
from .auth_serializer import CityListingSerializer


class UserProfileImageSerializer(serializers.ModelSerializer):
    """
    UserProfileImage serializer
    """

    profile_image = serializers.ImageField(required=True)

    class Meta:
        model = UserProfileImage
        fields = ["id", "user", "profile_image"]


class UserProfileSerializer(serializers.ModelSerializer):
    """
    UserProfileSerializer serializer
    """

    city = CityListingSerializer()
    single_profile_image = serializers.SerializerMethodField("get_single_profile_image")
    profile_images = serializers.SerializerMethodField()
    plans_attended = serializers.SerializerMethodField()
    plans_hosted = serializers.SerializerMethodField()
    instagram_posts = serializers.SerializerMethodField("get_instagram_posts")

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "full_name",
            "instagram_code",
            "city",
            "date_of_birth",
            "plans_attended",
            "plans_hosted",
            "single_profile_image",
            "profile_images",
            "instagram_posts",
        ]

    def get_single_profile_image(self, obj):
        request = self.context.get('request')
        images = UserProfileImage.objects.filter(user=obj.pk)
        if images.exists():
            image = images.first()
            return request.build_absolute_uri(image.profile_image.url)
        return ""

    def get_profile_images(self, instance):
        images = UserProfileImage.objects.filter(user=instance.pk)
        image_serializer = UserProfileImageSerializer(
            images, many=True, context={"request": self.context["request"]}
        )
        return image_serializer.data

    def get_plans_attended(self, instance):
        attendees = PlanJoiningRequest.objects.filter(user=instance.pk, status='ACCEPTED').count()
        return attendees

    def get_plans_hosted(self, instance):
        plans = Plan.objects.filter(user=instance.pk, active=True).count()
        return plans

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


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "full_name", "city", "date_of_birth"]

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
            instance.save()
        instance.save()
        return instance
