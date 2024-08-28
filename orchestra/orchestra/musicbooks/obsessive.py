import re
from email_validator import validate_email, EmailNotValidError
from django.db.models import IntegerField, ForeignKey, BooleanField, DateTimeField
from dateutil import parser
from datetime import datetime
import dns.resolver
import smtplib
from email.mime.text import MIMEText

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
        print("value :",value)
        print("type(value) :",type(value))
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
        
        if not key in modifiable_fields : 
            if key in non_string_fields :
                field_type = type(non_string_fields_data[non_string_fields.index(key)]).__name__
                if field_type == 'BooleanField': 
                    setattr(obj, key, interpret_boolean(value))
                elif field_type == 'IntegerField':
                    setattr(obj, key, int(value))
                elif field_type == 'DateField':
                    setattr(obj, key, parser.parse(value))

        if key in modifiable_fields :
            setattr(obj, key, clean_input(key,value))
    return obj