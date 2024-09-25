from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from orchestra.models import *
from orchestra.serializers import *
from rest_framework.authentication import TokenAuthentication  # Import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from orchestra.musicbooks.listener import Authentication
from googletrans import Translator, LANGUAGES
from orchestra.musicbooks.obsessive import *

class VidViewSet(viewsets.ModelViewSet):
    queryset = Vid.objects.all().order_by('-id')
    serializer_class = VidDefSer
    authentication_classes = [Authentication]  # Add TokenAuthentication

    @action(detail=False, methods=['POST'], authentication_classes=[Authentication])
    def add_vid(self, request, *args, **kwargs):

        user_input_url = request.data.get("url")
        urls = extract_youtube_urls(user_input_url)
        # Vid 모델의 url 필드에 이미 존재하는 URL들을 저장할 리스트
        
        urls, names = get_youtube_video_titles(urls)
        
        res = []
        for i in range(len(urls)) :
            res.append(
                {
                    "url":urls[i],
                    "name":names[i],
                }
            )
        return Response({'result': res}, 200)
    
    