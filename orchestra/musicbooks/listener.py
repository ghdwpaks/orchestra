from rest_framework import viewsets, filters, status, permissions, authentication, exceptions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from orchestra.models import *
from orchestra.serializers import *

from django.contrib.auth.hashers import check_password
from django.middleware.csrf import get_token
from .obsessive import get_input

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import random
import string
import boto3
from botocore.exceptions import NoCredentialsError


class Authentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        token = None
        try:
            token = UserToken.objects.select_related("user").get(key=key)
        except UserToken.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token.')
        if not token.useable : 
            raise exceptions.AuthenticationFailed('User Unuseabled.')
        elif token.user.is_active:
            raise exceptions.AuthenticationFailed('User Unactivated.')
        elif token.user.is_deleted: 
            raise exceptions.AuthenticationFailed('User deleted.')
        return (token.user, token)
    

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
        try:
            user = User.objects.get(uid=request.data.get("uid"))
            if user.check_password(request.data.get("password")):
                return Response({'token': UserToken.objects.get_or_create(user=user)[0].key})
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

        
    @action(detail=False, methods=['POST'])
    def sendEmailVerificationCode(self, request, *args, **kwargs):
        email = request.data.get("email")
        try : 
            User.objects.get(email=email)
        except User.DoesNotExist :
            return None
        
        random_string = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))

        message = Mail(
            from_email="hjm7904@gmail.com",
            to_emails=email,
            subject='String to be used for password change',
            html_content=f"""Your code is Here.
<strong>{random_string}</strong>"""
        )
        sg = SendGridAPIClient('your_sendgrid_api_key')
        response = sg.send(message)
    


    @action(detail=False, methods=['POST'])
    def send_email(self, request, *args, **kwargs):
        email = request.data.get("email")
        user = None
        try : 
            user = User.objects.get(email=email)
        except User.DoesNotExist :
            return Response({'result': False}, 200)


        random_string = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
        PasswordResetCode.objects.create(
            user = user,
            code = random_string
        )


        from_email = "hjm7904+1@gmail.com"
        to_emails = [email]
        subject = 'Test Subject'
        html_content = random_string
        client = boto3.client(
            'ses',
            region_name='ap-northeast-3',  # 적절한 AWS 리전으로 설정
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
        try:
            response = client.send_email(
                Source=from_email,
                Destination={'ToAddresses': to_emails},  # 리스트로 감싸줌
                Message={
                    'Subject': {'Data': subject},
                    'Body': {'Html': {'Data': html_content}}
                }
            )
            return Response({'result': True}, 200)
        except NoCredentialsError:
            return Response({'result': False}, 500)

    @action(detail=False, methods=['POST'])
    def confirm_email(self, request, *args, **kwargs):
        email = request.data.get("email")
        code = request.data.get("code")
        try : 
            passwordResetCode = PasswordResetCode.objects.get(
                    user=User.objects.get(email=email),
                    email=email,
                    code=code,
                    confirmable=True
                )
            passwordResetCode.confirmable = False
            passwordResetCode.save()
            return Response({'result': True}, 200)
        except User.DoesNotExist :
            return Response({'result': False}, 200)

    @action(detail=False, methods=['POST'])
    def change_password(self, request, *args, **kwargs):
        email = request.data.get("email")
        code = request.data.get("code")
        try : 
            user = User.objects.get(email=email)
            passwordResetCode = PasswordResetCode.objects.get(
                    user=user,
                    code=code,
                    confirmable=False,
                    useable=True
                )
            passwordResetCode.useable = False
            passwordResetCode.save()
            obj = get_input(
                    User,
                    request.data.items(),
                    user
                )
            
            obj.save()


            return Response({'result': True}, 200)
        except User.DoesNotExist :
            return Response({'result': False}, 200)
        
        




