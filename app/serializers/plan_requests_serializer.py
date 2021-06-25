from rest_framework import fields, serializers
from ..models import PlanJoiningRequest
from .auth_serializer import UserViewSerializer
from .plan_serializer import PlanDetailSerializer, PlanSerializer


class PlanJoiningRequestSerializer(serializers.ModelSerializer):
    """
    PlanJoiningRequest serializer
    """

    class Meta:
        model = PlanJoiningRequest
        fields = ["pk", "user", "plan", "status", "request_text", "response_text"]


class PlanRequestDetailSerializer(serializers.ModelSerializer):
    """
    PlanJoiningRequest serializer
    """
    user = UserViewSerializer()
    plan = PlanSerializer()

    class Meta:
        model = PlanJoiningRequest
        fields = ["pk", "user", "plan", "status", "request_text", "response_text"]


class PlanJoiningRequestListingSerializer(serializers.ModelSerializer):
    """
    PlanJoiningRequest serializer
    """
    user = UserViewSerializer()

    class Meta:
        model = PlanJoiningRequest
        fields = ["pk", "user", "plan", "status", "request_text", "response_text"]