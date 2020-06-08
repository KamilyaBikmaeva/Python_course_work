import hashlib
import random
import string

from django.db import models

# Create your models here.
from django.urls import reverse


class ShortLink(models.Model):
    full_link = models.TextField()
    shortened_link = models.TextField(null=True, blank=True)
    redirects = models.IntegerField()

    def generate_shortened_link(self):
        self.full_link = self.check_full_link(self.full_link)
        link = self.hash_generator(self)
        link = reverse('linker:redirect_view', kwargs={'short_link': link})
        self.shortened_link = link
        self.save(force_update=True)
        return self

    def get_absolute_url(self):
        return reverse('linker:result', kwargs={'link_id': self.id})

    @staticmethod
    def check_full_link(full_link):
        if full_link.startswith('http'):
            return full_link
        else:
            full_link = 'http://' + full_link
            return full_link

    @staticmethod
    def hash_generator(shortlink):
        salt = hashlib.md5(str(shortlink.full_link).encode('utf-8')).hexdigest()
        hash_link = hashlib.md5(str(shortlink.full_link + salt).encode('utf-8')).hexdigest()[:8]
        return hash_link

    def increment_redirects(self):
        self.redirects += 1
        self.save(force_update=True)