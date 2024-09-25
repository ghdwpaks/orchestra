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
    