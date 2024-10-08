# orchestra/urls.py
from django.contrib.auth import views as auth_views
from django.urls import path,re_path, include
from rest_framework import routers
from .musicbooks import magnifyer, listener, video, high, tag

class MenuitApiView(routers.APIRootView):pass

class DocumentedRouter(routers.DefaultRouter):
    APIRootView = MenuitApiView

router = DocumentedRouter()
router.register(r'magnifyer', magnifyer.ClefViewSet, basename="magnifyer")
router.register(r'listener', listener.ListenerViewSet, basename="listener")
router.register(r'vid', video.VidViewSet, basename="vid")
router.register(r'high', high.HighViewSet, basename="high")
router.register(r'tag', tag.TagViewSet, basename="tag")


urlpatterns = [
    re_path(r'^', include(router.urls)),
    # 기존 URL 패턴들
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
