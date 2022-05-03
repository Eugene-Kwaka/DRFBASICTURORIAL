from django.urls import path, include
from .views import  ModalViewSet, article_list, article_detail, ArticleAPIView, ArticleDetails, GenericAPIView,  ArticleViewSet, GenericViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('article', ModalViewSet, basename='article')

#router.register('article', ArticleViewSet, basename='article')
#router.register('article', GenericViewSet, basename='article')


urlpatterns = [
    path('', include(router.urls)),
    path('article/<int:pk>/', include(router.urls)),

# paths using the Class Based Views 
    #path('article/', ArticleAPIView.as_view()),
    #path('detail/<int:pk>/', ArticleDetails.as_view()),


    #path('generic/article/', GenericAPIView.as_view()),
    #path('generic/detail/<int:pk>/', GenericAPIView.as_view()),

]
