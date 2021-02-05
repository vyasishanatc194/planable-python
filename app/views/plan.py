from rest_framework.views import APIView
from planable.helpers import custom_response, serialized_response
from rest_framework import status
from planable.permissions import IsAccountOwner
from ..models import Plan, Category, PostalCode
from ..serializers import PlanCreateSerializer, CategoryListingSerializer, PostalCodeListingSerializer, PlanDetailSerializer


class PlanCreateAPIView(APIView):
    """
    User Sign up view
    """
    serializer_class = PlanCreateSerializer
    permission_classes = (IsAccountOwner,)

    def post(self, request, *args, **kwargs):
        request.data['user'] = request.user.pk
        message = "Plan created successfully!"
        serializer = self.serializer_class(data=request.data, context={'request': request})
        response_status, result, message = serialized_response(serializer, message)
        status_code = status.HTTP_201_CREATED if response_status else status.HTTP_400_BAD_REQUEST
        return custom_response(response_status, status_code, message, result)


class CategoryListingAPIView(APIView):
    """
    User Sign up view
    """
    serializer_class = CategoryListingSerializer
    permission_classes = ()

    def get(self, request):
        categories = Category.objects.filter(active=True)

        featured = request.GET.get('featured', None)
        if featured:
            categories = categories.filter(featured=True)

        serializer = self.serializer_class(categories, many=True, context={"request": request})
        message = "Categories fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)


class PostalCodeListingAPIView(APIView):
    """
    User Sign up view
    """
    serializer_class = PostalCodeListingSerializer
    permission_classes = ()

    def get(self, request):
        postal_codes = PostalCode.objects.filter(active=True)

        city = request.GET.get('city', None)
        if city:
            postal_codes = postal_codes.filter(city=city)

        serializer = self.serializer_class(postal_codes, many=True, context={"request": request})
        message = "Postal codes fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)


class PlanDetailAPIView(APIView):
    """
    User Sign up view
    """
    serializer_class = PlanDetailSerializer
    permission_classes = ()

    def get(self, request, pk):
        plan = Plan.objects.filter(active=True, pk=pk)
        if not plan:
            message = "Plan not found!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

        serializer = self.serializer_class(plan.first(), context={"request": request})
        message = "Plan detail fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)