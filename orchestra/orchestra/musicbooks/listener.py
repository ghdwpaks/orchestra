from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from orchestra.models import *
from orchestra.serializers import *
from .obsessive import get_input
class ListenerViewSet(viewsets.ModelViewSet):
    
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserDefSer

    @action(detail=False, methods=['POST'])
    def signUp(self, request, *args, **kwargs):
        print("*"*88)
        
        obj = get_input(
                User,
                request.data.items(),
                User()
            )
        
        obj.save()
        print("good to go")
        return Response({'result': UserDefSer(obj,many=False).data}, 200)
    

    
    @action(detail=False, methods=['POST'])
    def checkEmail(self, request, *args, **kwargs):
        if request.data.get("email") in User.objects.all().values_list("email",flat=True) :
            return Response({'result': False}, 200)
        else : 
            return Response({'result': True}, 200)

        

