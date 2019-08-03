from django.urls import path,include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [

    # ------------- class based CRUD operation with Authentication Permission ---------------#
    path('snippets/', views.ListApiSerializer.as_view(),name="list_snippets"),
    path('snippets/<int:pk>/', views.DetailListApiSerializer.as_view(),name="detailed_snippet"),
    path('snippets/create/', views.CreateSnippetSerializer.as_view(),name="create_snippet"),
    #----------------mixin based CRUD operation with Authentication Permission----------------#
    path('snippets/mixin/list/', views.SnippetClassList.as_view(),name=",mixin_list_snippet"),
    path('snippets/mixin/detail/<int:pk>/', views.SnippetClassDetail.as_view(),name="mixin_detailed_snippet"),
    #-------------- authenticatioin related users --------------#
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    #--------------- here we bind two serializers into one -------#
    path('', views.api_root),
    path('snippets/<int:pk>/highlight/', views.SnippetHighlight.as_view()),
    #------------ this will gives us login/logout option using  in browser--------#
    path('api-auth/', include('rest_framework.urls')),

]
# below suffixes are very important while you want to do specific type of
# like "http://127.0.0.1:8000/snippets/3.api" or "http://127.0.0.1:8000/snippets/3.json"
urlpatterns = format_suffix_patterns(urlpatterns)
