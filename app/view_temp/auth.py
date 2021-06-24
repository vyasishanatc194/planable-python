from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import JsonResponse
from ..models import User


class ResetPassword(TemplateView):
    template_name = 'forgot-password.html'
    def get(self,request,uid):
        user = User.objects.filter(password_reset_link=uid, is_active=True)
        if user:
            context = {'status':True,'uid':uid}
        else:
            context = {'status':False}
        return render(request,self.template_name,context)

    def post(self,request,uid):
        user = User.objects.filter(password_reset_link=uid,is_active=True)
        if not user:
            return JsonResponse({'status':False,'message':"User Not Found"})
        password = request.POST.get('password')

        user[0].set_password(password)
        user[0].password_reset_link = None
        user[0].save()
        response = {
            "message": "Password reset successful.",
            "status": True
        }
        return JsonResponse(response)

