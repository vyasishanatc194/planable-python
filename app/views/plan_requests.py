from rest_framework.views import APIView
from planable.helpers import custom_response, serialized_response
from rest_framework import status
from planable.permissions import IsAccountOwner
from ..models import PlanJoiningRequest, Plan
from ..serializers import PlanJoiningRequestSerializer, PlanRequestDetailSerializer, PlanJoiningRequestListingSerializer
import datetime


class PlanJoiningRequestAPIView(APIView):
    """
    Plan creation view
    """

    serializer_class = PlanJoiningRequestSerializer
    permission_classes = (IsAccountOwner,)

    def post(self, request, *args, **kwargs):
        plan = request.data.get("plan", None)
        if plan:
            valid_plan = Plan.objects.filter(
                pk=plan, plan_datetime__gte=datetime.datetime.now()
            )
            if not valid_plan:
                message = "Invalid Plan!"
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
        check_request = PlanJoiningRequest.objects.filter(
            plan=plan, user=request.user.pk
        )
        if check_request:
            result = {}
            plan_request = check_request.first()
            if plan_request.status == "PENDING":
                message = "You have already applied to join this plan! Your request is Pending"
            if plan_request.status == "DECLINED":
                message = "Your joining request has been declined!"
                result["response_text"] = plan_request.response_text
            if plan_request.status == "ACCEPTED":
                message = "Your joining request has already been accepted!"
            print("HERE", message)
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message, result)
        message = "Request Sent successfully!"
        data = request.data.copy()
        data["user"] = request.user.pk
        serializer = self.serializer_class(data=data, context={"request": request})
        response_status, result, message = serialized_response(serializer, message)
        status_code = (
            status.HTTP_201_CREATED if response_status else status.HTTP_400_BAD_REQUEST
        )
        return custom_response(response_status, status_code, message, result)


class AcceptDeclineJoiningRequestAPIView(APIView):
    """
    Plan creation view
    """

    serializer_class = PlanRequestDetailSerializer
    permission_classes = (IsAccountOwner,)

    def post(self, request, pk, *args, **kwargs):
        request_status = request.data.get("status", None)
        if not request_status:
            message = "Status field is required!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
        check_request = PlanJoiningRequest.objects.filter(pk=pk, plan__user=request.user.pk)
        if check_request:
            check_request[0].status = request_status
            check_request[0].response_text = request.data.get("response_text", None)
            check_request[0].save()

            serializer = self.serializer_class(
                check_request[0], context={"request": request}
            )
            message = f"Request status changed to {request_status} successfully!"
            serializer = self.serializer_class(check_request[0], context = {'request': request})
            return custom_response(True, status.HTTP_200_OK, message, serializer.data)
        message = "Invalid request ID!"
        return custom_response(False, status.HTTP_400_BAD_REQUEST, message)


    def get(self, request, pk, *args, **kwargs):
        check_request = PlanJoiningRequest.objects.filter(plan=pk)
        check_status = request.GET.get("status", None)
        if check_status:
            check_request = check_request.filter(status=check_status)
        serializer = PlanJoiningRequestListingSerializer(
            check_request, many=True, context={"request": request}
        )
        message = f"Joining requests fetched successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)