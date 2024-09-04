from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from orchestra.models import Vid
from orchestra.serializers import VidDefSer
from rest_framework.authentication import TokenAuthentication  # Import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from orchestra.musicbooks.listener import Authentication

class ClefViewSet(viewsets.ModelViewSet):
    queryset = Vid.objects.all().order_by('-id')
    serializer_class = VidDefSer
    authentication_classes = [Authentication]  # Add TokenAuthentication


    @action(detail=False, methods=['GET'])
    def dashboard(self, request, *args, **kwargs):
        # The method content remains the same
        vid = Vid.objects.all()
        if vid.exists():
            result = VidDefSer(vid, many=True).data
            return Response({'res': result}, 200)
        return Response({'res': []}, 200)
