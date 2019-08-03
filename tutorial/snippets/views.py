from django.shortcuts import render
from django.http import HttpResponse, JsonResponse,request
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Snippet
from .serializers import SnippetSerializer,SnippetModelSerializer
from rest_framework import serializers
from rest_framework.generics import RetrieveUpdateDestroyAPIView,ListAPIView,CreateAPIView
from rest_framework import permissions
from .permission import IsOwnerOrReadOnly

# ------------------ function based csrf permission---------
@csrf_exempt
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetModelSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetModelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
@csrf_exempt
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)


# ------------------ all class based views -------------------

class ListApiSerializer(ListAPIView):
    serializer_class = SnippetModelSerializer
    queryset = Snippet.objects.all()
class DetailListApiSerializer(RetrieveUpdateDestroyAPIView):
    serializer_class = SnippetModelSerializer
    queryset = Snippet.objects.all()
class CreateSnippetSerializer(CreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = SnippetModelSerializer
    queryset = Snippet.objects.all()


#---------------- using mixins ----------------------#
from rest_framework import mixins
from rest_framework import generics

class SnippetClassList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Snippet.objects.all()
    serializer_class = SnippetModelSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SnippetClassDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

#------------------ user based view API -------------
from django.contrib.auth.models import User
from .serializers import  UserSerializer
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# ----------------- Permission Related work  step by step implementation as below-----------
# in here only authenticated user can modify the data
# and unauthenticated just readonly the API
# steps need to perform
# 1. from rest_framework import permissions
# 2. add permission class field where you want to used  here
    # i added permission on SnippetClassList and SnippetClassDetail
    #    addthis=> "permission_classes = [permissions.IsAuthenticatedOrReadOnly]"
# 3. add login/logout option in on the urls
    # path('api-auth/', include('rest_framework.urls')),
# 4. then create file for permission.py in the app for special authenciation
    # then add with the permission_classes as argument example down below i created "IsOwnerOrReadOnly"
    # add this line whatever the place you want to authenication/ readonly access.
        # code=> permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })
from rest_framework import renderers
from rest_framework.response import Response

class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)