from django.urls import path, include
from .views import  ModalViewSet, article_list, article_detail, ArticleAPIView, ArticleDetails, GenericAPIView,  ArticleViewSet, GenericViewSet
# ViewSet functions are bundled to a url using Routers
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# this becomes the automatic home page for my api because I have specified it as such
router.register('article', ModalViewSet, basename='article')

#router.register('article', ArticleViewSet, basename='article')
#router.register('article', GenericViewSet, basename='article')


urlpatterns = [
# path that uses the Modal ViewSets
    path('', include(router.urls)),
    path('article/<int:pk>/', include(router.urls)),

# paths using the Viewsets and GenericViewSet
    # path('',include(router.urls)),
    # path('article/<int:pk>/', include(router.urls)),

# paths using the Class Based APIViews 
    #path('article/', ArticleAPIView.as_view()),
    #path('detail/<int:pk>/', ArticleDetails.as_view()),

# paths using the Generic APIViews and Mixins
    #path('generic/article/', GenericAPIView.as_view()),
    #path('generic/detail/<int:pk>/', GenericAPIView.as_view()),

]
