from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Story(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField()
    is_flag = models.BooleanField(default=False)
    votes = models.ManyToManyField(User, related_name="story_votes",
         through='UserVote', verbose_name="voting status")
    comments = models.ManyToManyField(User, related_name="story_comments",
         through='UserComment', verbose_name="comments")
    created_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title


class UserVote(models.Model):
    UPVOTE = 'upvote'
    DOWNVOTE = 'downvote'
    VOTE_STATUS = (
        (UPVOTE, 'UPVOTE'),
        (DOWNVOTE, 'DOWNVOTE')
    )
    user = models.ForeignKey(User)
    story = models.ForeignKey(Story, related_name="user_vote_story")
    status = models.CharField(choices=VOTE_STATUS, max_length=10)

    class Meta:
        unique_together = ("user", "story")


class UserComment(models.Model):
    user = models.ForeignKey(User)
    story = models.ForeignKey(Story, related_name="user_comment_story")
    comment = models.TextField()
