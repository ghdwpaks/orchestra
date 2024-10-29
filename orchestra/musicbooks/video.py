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
        update_channel_videos = request.data.get("update_channel_videos")

        if request.data.get("update_channel_videos") :
            ids = get_all_video_ids_from_channel()
            get_youtube_video_titles(None,ids)
        else : 
            user_input_url = request.data.get("url")
            urls = extract_youtube_urls(user_input_url)
            # Vid 모델의 url 필드에 이미 존재하는 URL들을 저장할 리스트
            
            get_youtube_video_titles(urls,None)
            
        return Response({'result': True}, 200)
    
    