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
from urllib.parse import urlparse, parse_qs

class HighViewSet(viewsets.ModelViewSet):
    queryset = High.objects.all().order_by('-id')
    serializer_class = HighDefSer
    authentication_classes = [Authentication]  # Add TokenAuthentication

    @action(detail=False, methods=['POST'], authentication_classes=[Authentication])
    def add_high(self, request, *args, **kwargs):
        timestamp = request.data.get("timestamp")
        # Vid 모델의 url 필드에 이미 존재하는 URL들을 저장할 리스트
        vid_id = request.data.get("vid_id")
        print("timestamp :",timestamp)

        if is_valid_youtube_url(timestamp) :
            timestamp = extract_timestamp(timestamp) #int
        else : 
            timestamp = convertTimeToSeconds(timestamp) #int
        
        if timestamp : 
            High.objects.create(
                vid = Vid.objects.get(id=vid_id),
                timestamp = timestamp
            )
        else : 
            return Response({'result': False}, 200)
        
        return Response({'result': True}, 200)
    
    @action(detail=False, methods=['POST'], authentication_classes=[Authentication])
    def del_high(self, request, *args, **kwargs):
        High.objects.filter(
            id = request.data.get("high_id"),
            vid_id = request.data.get("vid_id")
        ).delete()
        
        return Response({'result': True}, 200)
    
    @action(detail=False, methods=['GET'], authentication_classes=[Authentication])
    def get_highs(self, request, *args, **kwargs):
        return Response(
                {
                    'result': HighDetailSer(
                            High.objects.filter(
                                vid = Vid.objects.get(
                                    id=int(
                                            request.data.get("vid_id")
                                        )
                                    )
                            ),
                            many=True
                        ).data
                }, 
                200
            )
    









def convert_time_to_seconds(time_str):
    """
    t 파라미터는 다음과 같은 형식일 수 있음:
    - '45' (초)
    - '3m30s' (분 + 초)
    - '1h2m30s' (시 + 분 + 초)
    """
    if time_str is None:
        return 0
    
    total_seconds = 0
    current_value = ''
    
    for char in time_str:
        if char.isdigit():
            current_value += char
        else:
            if char == 'h':
                total_seconds += int(current_value) * 3600
            elif char == 'm':
                total_seconds += int(current_value) * 60
            elif char == 's':
                total_seconds += int(current_value)
            current_value = ''
    
    # 마지막에 남아있는 숫자가 초일 경우 처리
    if current_value:
        total_seconds += int(current_value)
    
    return total_seconds


def extract_video_info(youtube_url):
    # URL 파싱
    parsed_url = urlparse(youtube_url)
    
    # 1. 비디오 ID 추출 (youtu.be 또는 youtube.com)
    if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
        video_id = parse_qs(parsed_url.query).get('v', [None])[0]
    elif parsed_url.hostname == 'youtu.be':
        video_id = parsed_url.path[1:]
    else:
        return None, None
    
    # 2. 타임스탬프 추출
    time_str = parse_qs(parsed_url.query).get('t', [None])[0]
    timestamp = convert_time_to_seconds(time_str) if time_str else 0
    
    return video_id, timestamp


# 사용 예시
youtube_url = "https://youtu.be/0TCwx602Vlk?t=1h2m3s"
video_id, timestamp = extract_video_info(youtube_url)

if video_id is not None:
    print(f"Video ID: {video_id}")
    print(f"Timestamp: {timestamp} seconds")
else:
    print("Invalid YouTube URL")
