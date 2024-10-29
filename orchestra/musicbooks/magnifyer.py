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
from django.core.paginator import Paginator

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
        size = request.query_params.get('size')
        loc = request.query_params.get('loc')
        word = request.query_params.get('word')
        field = request.query_params.get('field')
        sort = request.query_params.get('sort')
        '''
        search_field
        tagname : 태그이름 부분포함검색
        vidname : 영상이름 부분포함검색
        '''

        print("l :",l)
        print("size :",size)
        print("loc :",loc)
        print("word :",word)
        print("field :",field)
        print("sort :",sort)

        if not word : word = ""
        if not field : field = ""
        l = 1 if not l else int(l)
        size = 10 if not size else int(size)
        loc = 1 if not loc else int(loc)



        q = Q()

        if word : 
            if field == "tag" :
                tagNames = TagName.objects.none()

                word_list = str(word).split(" ")
                for search_word in word_list :
                    tagNames = tagNames | TagName.objects.filter(name__contains=search_word)

                tagNames = tagNames.distinct().values_list("tag_id",flat=True)
                
                q |= Q(
                        id__in=Tag.objects.filter(
                                id__in=tagNames
                            ).values_list(
                                "tagMappers__vid_id",
                                flat=True
                            )
                    )

            elif field == "name" :
                q |= Q(
                        id__in=Vid.objects.filter(
                                name__contains=word
                            ).values_list(
                                "id",
                                flat=True
                            )
                    )
                
        #upd 업로드 최신순
        #upa 업로드 오래된순
        #idd id 최신순
        #ida id 오래된순
        
        vid = Vid.objects.filter(q)

        if sort == "upa" : vid = vid.order_by("upload_time")
        elif sort == "idd" : vid = vid.order_by("-id")
        elif sort == "ida" : vid = vid.order_by("id")
        else : vid = vid.order_by("-upload_time")



        vid = Paginator(vid, size)
        num_pages = vid.num_pages
        if loc > num_pages:
            loc = num_pages  # 페이지 번호를 최대 페이지로 조정
        elif loc < 1:
            loc = 1  # 페이지 번호가 1보다 작으면 1로 조정
        vid = vid.page(loc)
        

        context = {"l":l}

        

        print("num_pages :",num_pages)
        return Response({
                'result': VidDetailSer(vid, context=context,many=True).data,
                "l":l,
                "size":size,
                "loc":loc,
                "word":word,
                "field":field,
                "loc_limit":num_pages
            }, 200)
    
    
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
        


    