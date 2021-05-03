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
    profile_images = serializers.SerializerMethodField()
    plans_attended = serializers.SerializerMethodField()
    plans_hosted = serializers.SerializerMethodField()

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
            "profile_images",
        ]

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
