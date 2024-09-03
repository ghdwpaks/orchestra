from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from orchestra.models import *
from orchestra.serializers import *
from .obsessive import get_input
from django.contrib.auth.hashers import check_password
from django.middleware.csrf import get_token
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed

class ListenerViewSet(viewsets.ModelViewSet):
    
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserDefSer

    @action(detail=False, methods=['POST'])
    def signUp(self, request, *args, **kwargs):
        
        obj = get_input(
                User,
                request.data.items(),
                User()
            )
        
        obj.save()
        return Response({'result': UserDefSer(obj,many=False).data}, 200)


        
    @action(detail=False, methods=['POST'])
    def login(self, request, *args, **kwargs):
        print("entered")
        try:
            user = User.objects.get(email=request.data.get("email"))
            if user.check_password(request.data.get("password")):
                response = Response({"message": "Login successful"})
                csrf_token = get_token(request)
                response_data = {"message": "Login successful", "csrfToken": csrf_token}
                return Response(response_data)
                #response.set_cookie(
                #    "csrftoken", 
                #    csrf_token, 
                #    httponly=True,
                #    secure=True,  
                #    samesite='Lax'
                #)
                #return response
            else:
                raise AuthenticationFailed("Invalid User")
        except User.DoesNotExist:
            raise AuthenticationFailed("Invalid User")

    

    
    @action(detail=False, methods=['POST'])
    def checkEmail(self, request, *args, **kwargs):
        if request.data.get("email") in User.objects.all().values_list("email",flat=True) :
            return Response({'result': False}, 200)
        else : 
            return Response({'result': True}, 200)

        

