from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from orchestra.models import *
from orchestra.serializers import *
from orchestra.musicbooks.listener import Authentication
from orchestra.musicbooks.obsessive import *
from googletrans import Translator, LANGUAGES

def translate_text(text):
    translator = Translator()
    translations = [
        translator.translate(text, dest='ko').text,  # 한국어
        translator.translate(text, dest='en').text,  # 영어
        translator.translate(text, dest='ja').text   # 일본어
    ]
    return translations


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by('-id')
    serializer_class = TagDefSer
    authentication_classes = [Authentication]  # Add TokenAuthentication

    @action(detail=False, methods=['POST'], authentication_classes=[Authentication])
    def add_tag(self, request, *args, **kwargs):        
        user=self.request.user

        # The method content remains the same
        vid_id = int(request.data.get("vid_id"))
        name = request.data.get("name")
        if name : 
            l = int(request.data.get("l",1))

            vid = Vid.objects.get(id=vid_id)

            if TagName.objects.filter(
                tag_id__in=Tag.objects.filter(
                    id__in=TagMapper.objects.filter(
                            vid_id=vid.id
                        ).values_list('tag_id', flat=True)
                    ).values_list("id",flat=True),
                lang=l,
                name=name
                ).exists() :
                return Response({'result': "이미 값이 존재합니다."}, 200)
                
            tag = Tag.objects.create()

            TagMapper.objects.create(
                tag=tag,
                vid=vid
            )

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

        return Response({'result': True}, 200)
    
    @action(detail=False, methods=['POST'], authentication_classes=[Authentication])
    def del_tag(self, request, *args, **kwargs):
        # The method content remains the same
        vid_id = int(request.data.get("vid_id"))
        tag_id = int(request.data.get("tag_id"))

        TagMapper.objects.filter(
            vid_id=vid_id,
            tag_id=tag_id
            ).delete()
        
        #연결된 영상이 아무것도 없다면 박멸조치
        if not TagMapper.objects.filter(tag_id=tag_id).exists() :
            tags = Tag.objects.filter(id=tag_id)
            for tag in tags :
                TagName.objects.filter(tag_id=tag.id).delete()
            tags.delete()


        return Response({'result': True}, 200)