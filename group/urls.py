from django.urls import path
from .views import *

app_name = 'groups'

urlpatterns = [
    path('list/',GroupList.as_view(),name='group_list_url'),
    path('detail/<str:slug>-<int:pk>/',GroupDetail.as_view(),name='group_detail_url'),
    path('detail/<str:slug>-<int:pk>/enter/',GroupEnter.as_view(),name='group_enter_url'),
    path('detail/<str:slug>-<int:pk>/leave/',GroupLeave.as_view(),name='group_leave_url'),
    path('create/',GroupCreate.as_view(),name='group_create_url'),
    path('update/<str:slug>-<int:pk>/',GroupUpdate.as_view(),name='group_update_url'),
    path('delete/<str:slug>-<int:pk>/',GroupDelete.as_view(),name='group_delete_url'),
]
