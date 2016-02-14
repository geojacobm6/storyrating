"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib.auth.views import login
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from story.views import *

urlpatterns = [
    url(r'^login/$', login, {'template_name': 'admin/login.html'}),
    url(r'^admin/', admin.site.urls),
    url(r'^$', login_required(IndexView.as_view()), name='index'),
    url(r'^submit/$', login_required(StoryAdd.as_view()), name='story_add'),
    url(r'^story/(?P<pk>[0-9]+)/comments/$',
         login_required(StoryComments.as_view()), name='story_comments'),
    url(r'^story/(?P<pk>[0-9]+)/(?P<vtype>upvote|downvote)/$',
         login_required(StoryVote.as_view()), name='story_vote'),
]
