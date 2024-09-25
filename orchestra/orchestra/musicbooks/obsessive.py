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




def get_youtube_video_titles(url_list):
    # URL에서 비디오 ID를 추출하고 유효한 ID만 리스트로 만듦
    video_ids = []
    for url in url_list :
        video_id = extract_video_id(url)
        if not Vid.objects.filter(url=video_id).exists() :
            video_ids.append(video_id)

    # 비디오 ID들을 쉼표로 구분된 문자열로 변환
    video_ids_str = ','.join(video_ids)

    youtube_api_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_ids_str}&key={os.getenv('GOOGLE_ACCESS_KEY_ID')}"
    response = requests.get(youtube_api_url)
    video_data = response.json()
    
    channel_id = os.getenv('YOUTUBE_CHANNEL_ID')

    video_titles = []
    video_ids = []

    for item in video_data.get('items', []):
        if item['snippet']['channelId'] == channel_id:
            Vid.objects.create(
                name = item['snippet']['title'],
                url = item['id']
            )

            video_titles.append(item['snippet']['title'])
            video_ids.append(item['id'])

    return video_ids, video_titles



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