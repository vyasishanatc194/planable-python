from django.conf import settings
from rest_framework.views import APIView
from planable.helpers import custom_response, serialized_response
from rest_framework import status
from planable.permissions import IsAccountOwner
from ..models import Plan, Category, PostalCode, PlanJoiningRequest
from ..serializers import (
    PlanCreateSerializer,
    CategoryListingSerializer,
    PostalCodeListingSerializer,
    PlanDetailSerializer,
    HomeCategoryPlanListingSerializer,
)
import datetime
import pgeocode


class PlanCreateAPIView(APIView):
    """
    Plan creation view
    """

    serializer_class = PlanCreateSerializer
    permission_classes = (IsAccountOwner,)

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data["user"] = request.user.pk
        message = "Plan created successfully!"
        try:
            postal_code = request.data['postal_code']
            obj = PostalCode.objects.get(pk=postal_code)
            code = obj.postal_code
            nomi = pgeocode.Nominatim(settings.COUNTRY_CODE)
            lat = str(nomi.query_postal_code(code).latitude)
            long = str(nomi.query_postal_code(code).longitude)
            if (lat or long) == 'nan':
                lat = ''
                long = ''
        except Exception as inst:
            print(inst)
            lat = ''
            long = ''
        data['latitude'] = lat
        data['longitude'] = long
        serializer = self.serializer_class(
            data=data, context={"request": request}
        )
        response_status, result, message = serialized_response(serializer, message)
        status_code = (
            status.HTTP_201_CREATED if response_status else status.HTTP_400_BAD_REQUEST
        )
        return custom_response(response_status, status_code, message, result)


class CategoryListingAPIView(APIView):
    """
    Category listing View
    """

    serializer_class = CategoryListingSerializer
    permission_classes = ()

    def get(self, request):
        categories = Category.objects.filter(active=True)

        featured = request.GET.get("featured", None)
        if featured:
            categories = categories.filter(featured=True)

        serializer = self.serializer_class(
            categories, many=True, context={"request": request}
        )
        message = "Categories fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)


class PostalCodeListingAPIView(APIView):
    """
    Postal code listing view filtered by city
    """

    serializer_class = PostalCodeListingSerializer
    permission_classes = ()

    def get(self, request):
        postal_codes = PostalCode.objects.filter(active=True)

        city = request.GET.get("city", None)
        if city:
            postal_codes = postal_codes.filter(city=city)

        serializer = self.serializer_class(
            postal_codes, many=True, context={"request": request}
        )
        message = "Postal codes fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)


class PlanDetailAPIView(APIView):
    """
    Plan detail View
    """

    serializer_class = PlanDetailSerializer

    def get(self, request, pk):
        plan = Plan.objects.filter(active=True, pk=pk)
        if not plan:
            message = "Plan not found!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

        serializer = self.serializer_class(plan.first(), context={"request": request})
        message = "Plan detail fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)


class PlanListingAPIView(APIView):
    """
    Plan listing view with filters
    """

    serializer_class = PlanDetailSerializer
    permission_classes = ()

    def get(self, request):
        category = request.GET.get("category", None)
        search = request.GET.get("search", None)
        location = request.GET.get("location", None)
        today = request.GET.get("today", None)
        tomorrow = request.GET.get("tomorrow", None)
        plans = Plan.objects.filter(
            active=True, plan_datetime__gte=datetime.datetime.now()
        )
        if tomorrow:
            plans = plans.filter(
                plan_datetime__date=datetime.datetime.now() + datetime.timedelta(days=1)
            )
        if today:
            plans = plans.filter(plan_datetime__date=datetime.datetime.now())
        if category:
            plans = plans.filter(category=category)
        if search:
            plans = plans.filter(title__icontains=search)
        if location:
            plans = plans.filter(city__city__icontains=location)

        serializer = self.serializer_class(
            plans, many=True, context={"request": request}
        )
        message = "Plans fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)


class MyPlanListingAPIView(APIView):
    """
    My plans listing view
    """

    serializer_class = PlanDetailSerializer
    permission_classes = (IsAccountOwner,)

    def get(self, request):
        upcoming = request.GET.get("upcoming", None)
        user_id = request.GET.get("user_id", None)
        plans = Plan.objects.filter(active=True, user=request.user.pk)
        if user_id:
            plans = plans.filter(user=user_id)
        if upcoming:
            plans = plans.filter(plan_datetime__gte=datetime.datetime.now())
        serializer = self.serializer_class(
            plans, many=True, context={"request": request}
        )
        message = "Plans fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)


class HomePlanListingAPIView(APIView):
    """
    Plan listing view with filters
    """

    serializer_class = HomeCategoryPlanListingSerializer
    permission_classes = ()

    def get(self, request):
        categories = Category.objects.filter(featured=True)
        serializer = self.serializer_class(
            categories, many=True, context={"request": request}
        )
        message = "Plans fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)


class PlanAttendedAPIView(APIView):
    """
    My plans listing view
    """

    serializer_class = PlanDetailSerializer
    permission_classes = (IsAccountOwner,)

    def get(self, request):
        joining_requests = PlanJoiningRequest.objects.filter(user=request.user.pk, status="ACCEPTED")
        plans = []
        for joining_request in joining_requests:
            plans.append(joining_request.plan)
        serializer = self.serializer_class(
            plans, many=True, context={"request": request}
        )
        message = "Plans fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)