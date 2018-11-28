# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Msg_inbox(models.Model):
    sender = models.ForeignKey(User,related_name='sender')
    receiver = models.ForeignKey(User, related_name='receiver')
    msg_body = models.TextField()
    sent_time = models.DateTimeField()
    received_time = models.DateTimeField()
    def __str__(self):
        return unicode(self.sender) + u' ' + unicode(self.receiver)
    def __unicode__(self):
        return unicode(self.sender) + u' ' + unicode(self.receiver)