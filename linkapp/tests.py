import re

from django.test import TestCase
from .models import ShortLink

# Create your tests here.
from django.urls import reverse

class LinkTestCase(TestCase):
    def setUp(self):
        ShortLink.objects.create(full_link='example.com',
            shortened_link='test12test',
            redirects=0)

    def test_link_hash_generator(self):
        link = ShortLink.objects.get(id=1)
        self.assertIsNotNone(link.hash_generator(link))
        self.assertIsNotNone(re.match(r'^[\d\w]{8}$', link.hash_generator(link)))

    def test_link_check_full_link_add(self):
        link = ShortLink.objects.get(id=1)
        link.full_link = link.check_full_link(link.full_link)
        link.save()
        self.assertEqual(link.full_link, 'http://example.com')

    def test_link_check_full_link_no_add(self):
        link = ShortLink.objects.get(id=1)
        link.full_link = 'http://example.com'
        link.save()
        link.full_link = link.check_full_link(link.full_link)
        link.save()
        self.assertEqual(link.full_link, 'http://example.com')

    def test_link_get_absolute_url(self):
        link = ShortLink.objects.get(id=1)
        url = link.get_absolute_url()
        self.assertEqual(url, '/1/result/')

    def test_link_generate_shortened_link(self):
        link = ShortLink.objects.get(id=1)
        link.generate_shortened_link()
        link.save()
        print(link.shortened_link)
        self.assertIsNotNone(re.match(r'^/[\d\w]{8}/$', link.shortened_link))

    def test_redirect_view_link_redirects_incrementation(self):
        link = ShortLink.objects.get(id=1)
        link.increment_redirects()
        self.assertEqual(link.redirects, 1)

class URLTests(TestCase):
    def setUp(self):
        ShortLink.objects.create(full_link='http://example.com',
        shortened_link='/test12test/',
        redirects=0)

    def test_homepage(self):
        response = self.client.get(reverse('linker:main'))
        self.assertEqual(response.status_code, 200)

    def test_homepage_form_sending(self):
        response = self.client.post(reverse('linker:main'), data={'link': 'example.com'})
        self.assertEqual(response.status_code, 302)

    def test_result_page(self):
        response = self.client.get(reverse('linker:result', kwargs={'link_id': 1}))
        self.assertEqual(response.status_code, 200)

    def test_result_page_object_not_found_error(self):
        response = self.client.get(reverse('linker:result', kwargs={'link_id': 1001}))
        self.assertEqual(response.context['error'], True)

    def test_redirect_view(self):
        link = ShortLink.objects.get(shortened_link__contains='test12test')
        response = self.client.get(reverse('linker:redirect_view',
            kwargs={'short_link': link.shortened_link}))
        self.assertEqual(response.status_code, 302)

class ViewTests(TestCase):
    def test_main_page_template(self):
        response = self.client.get(reverse('linker:main'))
        self.assertEqual(response.templates[0].name, 'linkapp/main.html')

    def test_result_page_template(self):
        response = self.client.get(reverse('linker:result', kwargs={'link_id': 1}))
        self.assertEqual(response.templates[0].name, 'linkapp/result.html')

    def test_list_page_template(self):
        response = self.client.get(reverse('linker:list'))
        self.assertEqual(response.templates[0].name, 'linkapp/list.html')