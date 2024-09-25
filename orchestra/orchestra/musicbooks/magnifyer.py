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
        vid = Vid.objects.all()[:5]
        print("len(vid) :",len(vid))
        print("len(Vid.objects.all()) :",len(Vid.objects.all()))

        return Response({'result': VidDetailSer(vid, context=context,many=True).data}, 200)
    
    
    @action(detail=False, methods=['GET'], authentication_classes=[Authentication])
    def vid_detail(self, request, *args, **kwargs):
        user=self.request.user

        vid = Vid.objects.get(id=int(request.query_params.get('vid_id')))
        #High.objects.create(vid=vid,timestamp=83)

        context={
                "l":int(request.query_params.get('l',1))
            },
        result = {
            "vid" : VidDetailSer(
                    vid, 
                    context=context,
                    many=False
                ).data,
            "tag" : TagDetailSer(
                    Tag.objects.filter(
                        id__in=TagMapper.objects.filter(
                                vid_id=vid.id
                            ).values_list('tag_id', flat=True)
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
        
        return Response({'result': result}, 200)
        


    