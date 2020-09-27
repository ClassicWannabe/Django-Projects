from django.urls import path
from .views import *

app_name = 'posts'

urlpatterns = [
    path('create/',post_create,name='post_create_url'),
    path('list/',PostList.as_view(),name='post_list_url'),
    path('delete/<int:pk>/',PostDelete.as_view(),name='post_delete_url'),
    path('update/<int:pk>/',post_update,name='post_update_url'),
    path('detail/<int:pk>/',PostDetail.as_view(),name='post_detail_url'),
    path('<username>/',UserPosts.as_view(),name='user_post_list_url'),

]
