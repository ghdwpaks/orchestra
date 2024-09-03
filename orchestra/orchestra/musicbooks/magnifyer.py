from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from orchestra.models import *
from orchestra.serializers import *

class ClefViewSet(viewsets.ModelViewSet):
    
    queryset = Vid.objects.all().order_by('-id')
    serializer_class = VidDefSer

    @action(detail=False, methods=['GET'])
    def dashboard(self, request, *args, **kwargs):
        #user = self.request.user
        print("dashboard entered")
        result = {}
        vid = Vid.objects.all()
        if vid.exists() :
            result = VidDefSer(vid,many=True).data

        return Response({'res': result}, 200)

        

