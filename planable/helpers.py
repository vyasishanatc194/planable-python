from django.conf import settings
from rest_framework.pagination import PageNumberPagination
from firebase_dynamic_links import DynamicLinks
from rest_framework import status
from rest_framework.response import Response
import os
from app.models import User

# Pagination
PAGINATOR = PageNumberPagination()
PAGINATOR.page_size = 10
PAGINATOR_PAGE_SIZE = PAGINATOR.page_size


def custom_response(status_value, code, message, result={}):
    return Response({
                    'status': status_value,
                    'code': code,
                    'message': message,
                    'data': result
                }, status=status.HTTP_200_OK)


def dict_obj_list_to_str(data):
    for key, value in data.items():
        data[key] = "".join(value)
    return data


def get_pagination_response(model_class, request, serializer_class, context):
    result = {}
    model_response = PAGINATOR.paginate_queryset(model_class, request)
    serializer = serializer_class(model_response, many=True, context=context)
    result.update({'data':serializer.data})
    current = PAGINATOR.page.number
    next_page = 0 if PAGINATOR.get_next_link() is None else current + 1
    previous_page = 0 if PAGINATOR.get_previous_link() is None else current - 1
    result.update({'links': {
        'current': current,
        'next': next_page,
        'previous': previous_page,
        'total': PAGINATOR.page.paginator.count,
        'last' : PAGINATOR.page.paginator.num_pages,
    }})
    return result


def get_custom_pagination_response(model_class, request,message):
    result = {'status': True,'code': status.HTTP_200_OK,'message': message, 'data': None, 'links':None}
    model_response = PAGINATOR.paginate_queryset(model_class, request)
    result['data'] = model_response
    current = PAGINATOR.page.number
    next_page = 0 if PAGINATOR.get_next_link() is None else current + 1
    previous_page = 0 if PAGINATOR.get_previous_link() is None else current - 1
    result['links']={'current': current,
        'next': next_page,
        'previous': previous_page,
        'total': PAGINATOR.page.paginator.count,
        'last': PAGINATOR.page.paginator.num_pages,
    }
    return Response(result,status=status.HTTP_200_OK)



def serialized_response(serializer, message):
    if serializer.is_valid():
        serializer.save()
        result = serializer.data
        response_status = True
    else:
        result = dict_obj_list_to_str(serializer.errors)
        response_status = False
        message = "Please resolve error(s) OR fill Missing field(s)!"
    return response_status, result, message


def delete_media(path):
    media_root = getattr(settings, 'MEDIA_ROOT', None)
    if(os.path.exists(os.path.join(media_root, str(path))) and path):
        os.remove(os.path.join(media_root, str(path)))
    return True


def get_share_link(request):
    """Get shareable link"""

    url = request.build_absolute_uri()
    api_key = str(settings.FIREBASE_API_KEY)
    domain = str(settings.FIREBASE_DOMAIN)
    dl = DynamicLinks(api_key, domain)
    short_link = dl.generate_dynamic_link(url, True)
    return short_link
