from django.urls import path
from account.views import register_view,PostList,FilterList

from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('', register_view,name='register'),

    # login username and password (username=email, password=password)
    path('login',obtain_auth_token, name='login'),
    path('post',PostList.as_view(), name='post'),

    # end of url use  ?search=(name of item , you can search)
    path('list',FilterList.as_view(), name='filter')
]
