from rest_framework import fields, serializers
from ..models import Plan, Category, PostalCode, PlanJoiningRequest
from ..serializers import CityListingSerializer, UserViewSerializer
import datetime


class PlanJoiningRequestListingSerializer(serializers.ModelSerializer):
    """
    PlanJoiningRequest serializer
    """
    user = UserViewSerializer()

    class Meta:
        model = PlanJoiningRequest
        fields = ["pk", "user", "status"]



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
        ]


class CategoryListingSerializer(serializers.ModelSerializer):
    """
    Category serializer
    """

    class Meta:
        model = Category
        fields = ["id", "category_name", "featured"]


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

    city = CityListingSerializer()
    postal_code = PostalCodeListingSerializer()
    category = CategoryListingSerializer()
    user = UserViewSerializer()
    joinees = serializers.SerializerMethodField()
    hashtags = serializers.SerializerMethodField()
    request_status = serializers.SerializerMethodField()

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
            "joinees"
        ]

    def get_joinees(self, instance):
        joinees = PlanJoiningRequest.objects.filter(plan=instance, status='ACCEPTED')
        serializer = PlanJoiningRequestListingSerializer(joinees, many=True, context = {'request': self.context['request']})
        joinees_data = {}
        joinees_data['count'] = joinees.count()
        joinees_data['data'] = serializer.data
        return joinees_data

    def get_hashtags(self, instance):
        hashtags = instance.hashtags.split(",")
        formatted_hashtags = [hashtag.strip() for hashtag in hashtags]
        return formatted_hashtags

    def get_request_status(self, instance):
        user = self.context['request'].user
        if not user.is_anonymous:
            request_status = PlanJoiningRequest.objects.filter(plan=instance, user=user)
            if request_status:
                return request_status[0].status
        return False



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

