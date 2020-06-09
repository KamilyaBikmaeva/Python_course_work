import re

from django.test import TestCase
from .models import ShortLink

# Create your tests here.
from django.urls import reverse


class LinkTestCase(TestCase):
    """
        This class groups tests of ShortLink model
    """
    def setUp(self):
        ShortLink.objects.create(full_link='example.com',
            shortened_link='test12test',
            redirects=0)

    def test_link_hash_generator(self):
        """Assert hash generator works and generates hash"""
        link = ShortLink.objects.get(id=1)
        self.assertIsNotNone(link.hash_generator(link))
        self.assertIsNotNone(re.match(r'^[\d\w]{8}$', link.hash_generator(link)))

    def test_link_check_full_link_add(self):
        """Assert check_full_link method adds 'http://' to link if none"""
        link = ShortLink.objects.get(id=1)
        link.full_link = link.check_full_link(link.full_link)
        link.save()
        self.assertEqual(link.full_link, 'http://example.com')

    def test_link_check_full_link_no_add(self):
        """Assert check_full_link method doesn't add anything if protocol signature already exist"""
        link = ShortLink.objects.get(id=1)
        link.full_link = 'http://example.com'
        link.save()
        link.full_link = link.check_full_link(link.full_link)
        link.save()
        self.assertEqual(link.full_link, 'http://example.com')

    def test_link_get_absolute_url(self):
        """Assert get_absolute_url method returns URL to"""
        link = ShortLink.objects.get(id=1)
        url = link.get_absolute_url()
        self.assertEqual(url, '/1/result/')

    def test_link_generate_shortened_link(self):
        """Assert method in model generates short link"""
        link = ShortLink.objects.get(id=1)
        link.generate_shortened_link()
        link.save()
        print(link.shortened_link)
        self.assertIsNotNone(re.match(r'^/[\d\w]{8}/$', link.shortened_link))

    def test_redirect_view_link_redirects_incrementation(self):
        """Assert redirects counter works"""
        link = ShortLink.objects.get(id=1)
        link.increment_redirects()
        self.assertEqual(link.redirects, 1)

class URLTests(TestCase):
    """
        This class groups tests for URL routing
    """
    def setUp(self):
        ShortLink.objects.create(full_link='http://example.com',
        shortened_link='/test12test/',
        redirects=0)

    def test_homepage(self):
        """Assert main page is served well"""
        response = self.client.get(reverse('linker:main'))
        self.assertEqual(response.status_code, 200)

    def test_homepage_form_sending(self):
        """Assert form action causes redirect to result page"""
        response = self.client.post(reverse('linker:main'), data={'link': 'example.com'})
        self.assertEqual(response.status_code, 302)

    def test_result_page(self):
        """Assert result page is available"""
        response = self.client.get(reverse('linker:result', kwargs={'link_id': 1}))
        self.assertEqual(response.status_code, 200)

    def test_result_page_object_not_found_error(self):
        """Assert error showed when model with given ID is not found (not created yet)"""
        response = self.client.get(reverse('linker:result', kwargs={'link_id': 1001}))
        self.assertEqual(response.context['error'], True)

    def test_redirect_view(self):
        """Assert redirect sent on short link click"""
        link = ShortLink.objects.get(shortened_link__contains='test12test')
        response = self.client.get(reverse('linker:redirect_view',
            kwargs={'short_link': link.shortened_link}))
        self.assertEqual(response.status_code, 302)

class ViewTests(TestCase):
    """
        This class groups tests of needed templates used for render
    """
    def test_main_page_template(self):
        response = self.client.get(reverse('linker:main'))
        self.assertEqual(response.templates[0].name, 'linkapp/main.html')

    def test_result_page_template(self):
        response = self.client.get(reverse('linker:result', kwargs={'link_id': 1}))
        self.assertEqual(response.templates[0].name, 'linkapp/result.html')

    def test_list_page_template(self):
        response = self.client.get(reverse('linker:list'))
        self.assertEqual(response.templates[0].name, 'linkapp/list.html')