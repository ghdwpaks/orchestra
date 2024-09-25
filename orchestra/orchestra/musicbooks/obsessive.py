import re
from email_validator import validate_email, EmailNotValidError
from django.db.models import IntegerField, ForeignKey, BooleanField, DateTimeField
from dateutil import parser
from datetime import datetime
import dns.resolver
import smtplib
from rest_framework.response import Response
from email.mime.text import MIMEText
from googleapiclient.discovery import build
import re
import os
import requests
from django.http import JsonResponse
from django.conf import settings
from urllib.parse import urlparse, parse_qs
from orchestra.models import Vid

API_KEY = os.getenv('GOOGLE_ACCESS_KEY_ID')

def clean_html(input_text):
    # HTML 태그 제거
    clean_text = re.sub(r'<[^>]*>', '', input_text)
    # 스크립트 태그 제거
    clean_text = re.sub(r'<script.*?</script>', '', clean_text, flags=re.DOTALL)
    return clean_text

def clean_input(key,value):
    value = clean_html(value)
    if "email" in key :
        value = validate_email(value).email
        pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        if not pattern.match(value):
            raise EmailNotValidError
        
        if not dns.resolver.resolve(value.split('@')[-1], 'MX'):
            raise EmailNotValidError
    
    return value





def interpret_boolean(user_input):
    # 소문자로 변환하여 일관된 비교를 위해 정규화
    normalized_input = str(user_input).strip().lower()
    
    # 긍정적 의미의 입력 처리
    true_values = {'yes', 'true', '1', 'on', 'enable', 'enabled'}
    # 부정적 의미의 입력 처리
    false_values = {'no', 'false', '0', 'off', 'disable', 'disabled'}
    
    if normalized_input in true_values:
        return True
    elif normalized_input in false_values:
        return False
    else:
        return False


    
def get_input(model,items,obj) :
    
    model_fields = [field for field in model._meta.get_fields() if field.concrete]
    fields_list = [field.name for field in model_fields]

    non_string_fields = [] # text 로 그대로 넣으면 안되는 값들
    non_string_fields_data = []
    for field in model_fields:
        if isinstance(field, (ForeignKey, BooleanField, IntegerField, DateTimeField)):
            non_string_fields.append(field.name)
            non_string_fields_data.append(field)


    modifiable_fields = model.get_api_modifiable_fields()

    for key, value in items:
        if key in modifiable_fields : 
            if key in non_string_fields :
                field_type = type(non_string_fields_data[non_string_fields.index(key)]).__name__
                if field_type == 'BooleanField': 
                    setattr(obj, key, interpret_boolean(value))
                elif field_type == 'IntegerField':
                    setattr(obj, key, int(value))
                elif field_type == 'DateField':
                    setattr(obj, key, parser.parse(value))
            else : 
                setattr(obj, key, clean_input(key,value))
        else :
            if key == 'password':  # 비밀번호는 해싱하여 저장
                obj.set_password(value)
    return obj


def is_hashed(text):
    # 정규 표현식을 사용하여 다양한 해시 형식을 확인
    patterns = {
        'MD5': r'^[a-f0-9]{32}$',
        'SHA1': r'^[a-f0-9]{40}$',
        'SHA256': r'^[a-f0-9]{64}$',
        'Argon2': r'^\$argon2[a-z0-9]{1,}\$v=\d+\$m=\d+,t=\d+,p=\d+\$[a-zA-Z0-9+/=]+\$[a-zA-Z0-9+/=]+$'  # Argon2 해시 패턴
    }
    
    # 각 패턴에 대해 입력된 문자열이 일치하는지 확인
    for hash_type, pattern in patterns.items():
        if re.match(pattern, text):
            return True
    
    return False

def extract_youtube_urls(text):
    if text :
        # Regular expression to match YouTube URLs
        youtube_regex = (
            r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
            r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
        
        # Find all matches in the text
        matches = re.findall(youtube_regex, text)
        
        # Build the list of full URLs
        youtube_urls = []
        for match in matches:
            # Construct the full YouTube URL from the captured groups
            full_url = f"https://www.youtube.com/watch?v={match[5]}"
            youtube_urls.append(full_url)
        
        return youtube_urls
    return Response({'result': "이미 값이 존재합니다."}, 500)

def get_youtube_thumbnail(video_id):
    ampersand_position = video_id.find('&')
    if ampersand_position != -1:
        video_id = video_id[:ampersand_position]
    
    # 작은 썸네일 URL 생성
    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/default.jpg"
    
    return thumbnail_url




def get_youtube_video_titles(url_list,video_ids):
    # URL에서 비디오 ID를 추출하고 유효한 ID만 리스트로 만듦
    if not video_ids :
        video_ids = []
        for url in url_list :
            video_id = extract_video_id(url)
            if not Vid.objects.filter(url=video_id).exists() :
                video_ids.append(video_id)



    for i in range(0, len(video_ids), 50):
        # 50개의 동영상 ID로 분할하여 요청
        video_ids_chunk = video_ids[i:i + 50]
        video_ids_str = ','.join(video_ids_chunk)
        
        # API 요청 URL
        youtube_api_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_ids_str}&key={API_KEY}"
        
        # API 요청 보내기
        response = requests.get(youtube_api_url)
        video_data = response.json()

        # 동영상 정보를 저장하는 로직
        for item in video_data.get('items', []):
            if item['snippet']['channelId'] == os.getenv('YOUTUBE_CHANNEL_ID'):
                Vid.objects.create(
                    name=item['snippet']['title'],
                    url=item['id']
                )



def extract_video_id(youtube_url):
    # URL 파싱
    parsed_url = urlparse(youtube_url)

    
    # 1. youtube.com/watch?v= 형태 처리
    if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
        query_params = parse_qs(parsed_url.query)
        return query_params.get('v', [None])[0]
    
    # 2. youtu.be/ 형태 처리
    elif parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    
    # URL이 비디오 ID를 포함하지 않는 경우
    return None



def extract_timestamp(youtube_url):
    # URL 파싱
    parsed_url = urlparse(youtube_url)
    
    # 쿼리 파라미터 추출 (일반 URL일 경우)
    query_params = parse_qs(parsed_url.query)

    # 단축 URL일 경우, 쿼리 파라미터는 없고 fragment에 있을 수 있음
    if not query_params and parsed_url.fragment:
        query_params = parse_qs(parsed_url.fragment)
    
    # 타임스탬프가 't' 파라미터에 존재하는지 확인
    if 't' in query_params:
        time_str = query_params['t'][0]  # 첫 번째 값을 가져옴
        return convert_time_to_seconds(time_str)
    
    return 0  # 타임스탬프가 없을 경우 0초로 반환

def convert_time_to_seconds(time_str):
    """
    t 파라미터는 다음과 같은 형식일 수 있음:
    - '45' (초)
    - '3m30s' (분 + 초)
    - '1h2m30s' (시 + 분 + 초)
    """
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





def is_valid_youtube_url(url):
    if isinstance(url, str) :
        """
        입력된 URL이 YouTube URL인지 판별하는 함수
        """
        # YouTube URL 패턴
        youtube_regex = (
            r'(https?://)?(www\.)?'
            '(youtube|youtu|youtube-nocookie)\.(com|be)/'
            '(watch\?v=|embed/|v/|.+\?v=|shorts/|watch\?v=)?([^&=%\?]{11})')
        
        # 정규 표현식으로 URL 매칭
        match = re.match(youtube_regex, url)
        
        # 매칭이 되는지 확인
        return bool(match)
    else : 
        return False


def convertTimeToSeconds(timeStr):
    if str(timeStr).isdigit() : 
        return int(timeStr)
    # 정규 표현식을 사용하여 시간 형식을 추출 (시, 분, 초를 나타내는 부분을 처리)
    timePattern = r'(?P<value>\d+)(?P<unit>[hms시분초]?)'

    # 정규식으로 시, 분, 초를 파싱
    matches = re.findall(timePattern, timeStr)

    totalSeconds = 0
    
    for value, unit in matches:
        value = int(str(value).strip())
        
        # 단위에 따른 계산 (영어와 한글 둘 다 처리)
        if unit in ['h', '시']:
            totalSeconds += value * 3600
        elif unit in ['m', '분']:
            totalSeconds += value * 60
        elif unit in ['s', '초'] or unit == '':
            totalSeconds += value
    
    return totalSeconds













import requests
import os

# YouTube Data API v3 key 설정 (Google Cloud Console에서 생성된 API 키)


# 채널의 모든 동영상 ID를 가져오는 함수
def get_all_video_ids_from_channel():
    uploads_playlist_id = get_uploads_playlist_id(os.getenv('YOUTUBE_CHANNEL_ID'))
    video_ids = get_video_ids_from_playlist(uploads_playlist_id)
    
    return video_ids


# 채널 ID로 업로드된 동영상 재생목록 ID 가져오기
def get_uploads_playlist_id(channel_id):
    url = f"https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id={channel_id}&key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['items']:
            # 채널의 업로드된 동영상 재생목록 ID
            return data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    return None

# 재생목록에서 모든 동영상 ID 가져오기
def get_video_ids_from_playlist(playlist_id):
    video_ids = []
    base_url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&playlistId={playlist_id}&maxResults=50&key={API_KEY}"
    
    next_page_token = None
    
    while True:
        url = base_url + (f"&pageToken={next_page_token}" if next_page_token else "")
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            video_ids.extend(item['contentDetails']['videoId'] for item in data['items'])
            next_page_token = data.get('nextPageToken')
            if not next_page_token:
                break
        else:
            break
    return video_ids

