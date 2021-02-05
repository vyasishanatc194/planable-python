from rest_framework import fields, serializers
from ..models import Plan, Category, PostalCode
from ..serializers import CityListingSerializer, UserViewSerializer


class PlanCreateSerializer(serializers.ModelSerializer):
    """
    PlanCreateSerializer serializer
    """
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    plan_date = serializers.CharField(required=True)
    plan_time = serializers.CharField(required=True)
    location = serializers.CharField(required=True)
    spaces_available = serializers.IntegerField(required=True)


    class Meta:
        model = Plan
        fields = ['title', 'user', 'description', 'plan_date', 'plan_time', 'location', 'city', 'postal_code', 'spaces_available', 'category', 'plan_image', 'hashtags']


class CategoryListingSerializer(serializers.ModelSerializer):
    """
    Category serializer
    """
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'featured']


class PostalCodeListingSerializer(serializers.ModelSerializer):
    """
    PostalCode serializer
    """
    class Meta:
        model = PostalCode
        fields = ['id', 'city', 'postal_code']


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

    class Meta:
        model = Plan
        fields = ['title', 'user', 'description', 'plan_date', 'plan_time', 'location', 'joinees', 'city', 'postal_code', 'spaces_available', 'category', 'plan_image', 'hashtags']

    def get_joinees(self, instance):
        #TODO count total users whoc joined plan
        return 0

    def get_hashtags(self, instance):
        hashtags = instance.hashtags.split(',')
        return hashtags