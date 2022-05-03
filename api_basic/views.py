from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser

from .models import Article
from .serializers import ArticleSerializer
#This decorator function enabled us to create webrowsable api_views
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework import status
# Subclasses the normal view classes
from rest_framework.views import APIView
#Used in writing GENERIC VIEWS & MIXINS
from rest_framework import generics 
from rest_framework import mixins 
#These modules are for AUTHENTICATION
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication 
from rest_framework.permissions import IsAuthenticated
#Enables me to write Viewset API classes
from rest_framework import viewsets 
# Shorcut to access an object from a queryset
from django.shortcuts import get_object_or_404




#################################################################################################################################################################



#MODAL VIEWSETS
class ModalViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()



#GENERIC VIEWSETS
class GenericViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()


#VIEWSETS AND ROUTERS
class ArticleViewSet(viewsets.ViewSet):
    # GET REQUES
    def list(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Article.objects.all()
        article = get_object_or_404(queryset, pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def update(self, request, pk=None):
        article = Article.objects.get(pk)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        article = Article.objects.get(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



#################################################################################################################################################################



# GENERIC APIVIEWS AND MIXINS
class GenericAPIView(generics.GenericAPIView,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    lookup_field = 'pk'
    #authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request):

        return self.create(request)

    def put(self, request, pk=None):

        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)


#################################################################################################################################################################

# CLASS-BASED APIVIEWS
""" The same code in FBVs is used in the CBVs """
class ArticleAPIView(APIView):
    # GET request given its own function 
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ArticleDetails(APIView):
    # Place the try % except method in a function called get_object 
    def get_object(self, pk):
        try:
            return Article.objects.get(pk=pk)

        except Article.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        # I get the article object from the get_object function using self
        article = self.get_object(pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        article = self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#################################################################################################################################################################


#FUNCTION-BASED APIVIEWS
""" The same code in FBVs is used in the CBVs """
@api_view(['GET', 'POST'])
def article_list(request):

    if request.method == "GET":
        #lists the all the articles in the db 
        articles = Article.objects.all()
        # serializing a queryset requires the many=True
        #serializing the article objects inti json
        serializer = ArticleSerializer(articles, many=True)
        # return response either as browsable API or json
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = ArticleSerializer(data=request.data)
        # if the serializer is valid I need to save 
        if serializer.is_valid():
            serializer.save()
            # return a response with a status that artices have been created
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Else return error 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT', 'DELETE'])
def article_detail(request, pk):
    try:
        # To access that individual article I want from the db
        article = Article.objects.get(pk=pk)
    # if tyhe article does not exist then return a response that the article not found
    except Article.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    elif request.method == "DELETE":
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
