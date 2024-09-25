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

def translate_text(text):
    translator = Translator()
    translations = [
        translator.translate(text, dest='ko').text,  # 한국어
        translator.translate(text, dest='en').text,  # 영어
        translator.translate(text, dest='ja').text   # 일본어
    ]
    return translations





class ClefViewSet(viewsets.ModelViewSet):
    queryset = Vid.objects.all().order_by('-id')
    serializer_class = VidDefSer
    authentication_classes = [Authentication]  # Add TokenAuthentication


    @action(detail=False, methods=['GET'], authentication_classes=[Authentication])
    def dashboard(self, request, *args, **kwargs):
        # The method content remains the same
        l = request.query_params.get('l')
        context = {
            "l":l
        }
        result = {}
        vid = Vid.objects.all()
        return Response({'result': VidDetailSer(vid, context=context,many=True).data}, 200)
    
    
    @action(detail=False, methods=['GET'], authentication_classes=[Authentication])
    def vid_detail(self, request, *args, **kwargs):
        user=self.request.user

        vid = Vid.objects.get(id=int(request.query_params.get('vid_id')))
        #High.objects.create(vid=vid,timestamp=83)

        h = High.objects.filter(vid_id=vid.id)
        hds = HighDetailSer(h, context={'request': request}, many=True).data
        context={
                "l":int(request.query_params.get('l'))
            },
        

        result = {
            "vid" : VidDetailSer(
                    vid, 
                    context=context,
                    many=False
                ).data,
            "tag" : TagDetailSer(
                    Tag.objects.filter(
                            vid_id=vid.id
                        ), 
                    context=context,
                    many=True
                ).data,
            "high" : HighDetailSer(
                    High.objects.filter(
                            vid_id=vid.id
                        ), 
                    many=True
                ).data,
            }
        

        print("request :",request)
        return Response({'result': result}, 200)
        


    
    @action(detail=False, methods=['POST'], authentication_classes=[Authentication])
    def add_tag(self, request, *args, **kwargs):
        
        user=self.request.user


        # The method content remains the same
        vid_id = int(request.data.get("vid_id"))
        name = request.data.get("name")
        l = int(request.data.get("l"))

        vid = Vid.objects.get(vid_id=vid_id)

        if TagName.objects.filter(
            tag_id__in=Tag.objects.filter(
                    vid_id=vid.id
                ).values_list("id",flat=True),
            lang=l,
            name=name
            ).exists() :
            return Response({'result': "이미 값이 존재합니다."}, 500)
            
        tag = Tag.objects.create(
            user=user,
            vid=vid
        )
        translate_text
        TagName.objects.create(
            user=user,
            tag=tag,
            lang=l,
            name=name
        )
        language_ids = [l-1 for l in [
                1-1, 
                2-1, 
                3-1
            ]] #l 을 제외한 나머지 언어만 번역 적용
        
        translated_text = translate_text(name)
        for language_id in language_ids :
            TagName.objects.create(
                user=user,
                tag=tag,
                lang=language_id,
                name=translated_text[language_id]
            )
            #번역된 태그내용들 추가

        TagDefSer(tag,context=context,many=False).data
        context = {
            "l":l
        }
        return Response({'result': TagDefSer(tag,context=context,many=False).data}, 200)
    

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