from rest_framework import fields, serializers
from ..models import Plan, Category, PostalCode, PlanJoiningRequest, UserProfileImage
from ..serializers import CityListingSerializer, UserViewSerializer
import datetime
from planable.helpers import get_share_link


class PlanJoiningRequestListingSerializer(serializers.ModelSerializer):
    """
    PlanJoiningRequest serializer
    """
    user = UserViewSerializer()
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = PlanJoiningRequest
        fields = ["pk",
            "user",
            "status",
            "profile_image"
        ]

    def get_profile_image(self, instance):
        request = self.context.get('request')
        user_images = UserProfileImage.objects.filter(user=instance.user)
        if user_images:
            image = user_images.first()
            return request.build_absolute_uri(image.profile_image.url)
        return None


class PlanCreateSerializer(serializers.ModelSerializer):
    """
    PlanCreateSerializer serializer
    """

    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    plan_datetime = serializers.DateTimeField(required=True)
    location = serializers.CharField(required=True)
    spaces_available = serializers.IntegerField(required=True)

    class Meta:
        model = Plan
        fields = [
            "title",
            "user",
            "description",
            "plan_datetime",
            "location",
            "city",
            "postal_code",
            "spaces_available",
            "category",
            "plan_image",
            "hashtags",
            "latitude",
            "longitude"
        ]


class CategoryListingSerializer(serializers.ModelSerializer):
    """
    Category serializer
    """

    class Meta:
        model = Category
        fields = ["id", "category_name", "category_image", "featured"]


class PostalCodeListingSerializer(serializers.ModelSerializer):
    """
    PostalCode serializer
    """

    class Meta:
        model = PostalCode
        fields = ["id", "city", "postal_code"]


class PlanDetailSerializer(serializers.ModelSerializer):
    """
    Plan Detail serializer
    """

    plan_datetime = serializers.SerializerMethodField()
    city = CityListingSerializer()
    # postal_code = PostalCodeListingSerializer()
    category = CategoryListingSerializer()
    user = UserViewSerializer()
    joinees = serializers.SerializerMethodField()
    hashtags = serializers.SerializerMethodField()
    request_status = serializers.SerializerMethodField()
    share_link = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = [
            "id",
            "title",
            "user",
            "description",
            "plan_datetime",
            "location",
            "city",
            "postal_code",
            "spaces_available",
            "category",
            "plan_image",
            "hashtags",
            "request_status",
            "joinees",
            "latitude",
            "longitude",
            "share_link"
        ]

    def get_plan_datetime(self, instance):
        return f"{instance.plan_datetime.date()} {instance.plan_datetime.time()}"

    def get_joinees(self, instance):
        joinees = PlanJoiningRequest.objects.filter(plan=instance, status='ACCEPTED')
        serializer = PlanJoiningRequestListingSerializer(joinees, many=True, context = {'request': self.context['request']})
        joinees_data = {}
        joinees_data['count'] = joinees.count()
        joinees_data['data'] = serializer.data
        return joinees_data

    def get_hashtags(self, instance):
        if instance.hashtags:
            hashtags = instance.hashtags.split(",")
            formatted_hashtags = [hashtag.strip() for hashtag in hashtags]
            return formatted_hashtags
        return []

    def get_request_status(self, instance):
        user = self.context['request'].user
        if not user.is_anonymous:
            request_status = PlanJoiningRequest.objects.filter(plan=instance, user=user)
            if request_status:
                return request_status[0].status
        return False

    def get_share_link(self, obj):
        """Get Plan share link"""
        if obj.share_link:
            return obj.share_link
        try:
            request = self.context.get('request')
            short_link = get_share_link(request)
            obj.share_link = short_link
            obj.save()
            return short_link
        except Exception as inst:
            print(inst)
            return ""


class HomeCategoryPlanListingSerializer(serializers.ModelSerializer):
    """
    Home Category plan serializer
    """
    plans = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ["id", "category_name", "featured", "plans"]

    def get_plans(self, instance):
        plans = Plan.objects.filter(active=True, plan_datetime__gte=datetime.datetime.now(), category=instance)[:5]   
        serializer = PlanDetailSerializer(plans, many=True, context={'request': self.context['request']})
        return serializer.data

