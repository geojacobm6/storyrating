from datetime import datetime, timedelta
from django.db.models import IntegerField, Sum, Case, When
from django.shortcuts import render, redirect
from django.views import generic

from story.models import Story, UserVote, UserComment


class IndexView(generic.ListView):
    template_name = 'index.html'
    model = Story

    def get_queryset(self):
        rating = UserVote.objects.values('story').annotate(
            upvote=Sum(
                Case(When(status=UserVote.UPVOTE, then=1),
                    output_field=IntegerField())
                    ),
            downvote=Sum(
                Case(When(status=UserVote.DOWNVOTE, then=1),
                    output_field=IntegerField())
                    )
            )
        rating = sorted(rating, key=lambda k: k['upvote'], reverse=True)
        filter_key = {'is_flag': False}
        if 'duration' in list(self.request.GET.keys()):
            filter_key['created_on__gte'] = datetime.now() -\
             timedelta(hours=int(self.request.GET['duration']))

        objects = Story.objects.filter(**filter_key)
        objects = dict([(obj.id, obj) for obj in objects])
        sorted_objects = [objects[id['story']] for id in rating]
        return sorted_objects[:5]

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        total = []
        for obj in context['object_list']:
            if obj.user_vote_story.all()\
            .filter(user_id=self.request.user.id).exists():
                total.append({'story': obj,
                     'vote': obj.user_vote_story.all()
                     .filter(user_id=self.request.user.id)[0].status})
            else:
                total.append({'story': obj,
                     'vote': None})
        context['total'] = total
        return context


class StoryAdd(generic.CreateView):
    model = Story
    fields = ['title', 'link']
    success_url = '/'


class StoryComments(generic.View):

    def get(self, request, pk):
        data = {'status': 'failed'}
        data['story'] = Story.objects.get(id=pk)
        return render(request, 'story/story_comments.html', data)

    def post(self, request, pk):
        data = {'status': 'failed'}
        data['story'] = story = Story.objects.get(id=pk)
        UserComment.objects.create(story=story, user=request.user,
             comment=request.POST['comment'])
        return render(request, 'story/story_comments.html', data)


class StoryVote(generic.View):

    def get(self, request, pk, vtype):
        story = Story.objects.get(id=pk)
        vote, created = UserVote.objects.get_or_create(story=story,
             user=request.user)
        vote.status = vtype
        vote.save()
        return redirect('/')