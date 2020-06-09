from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ShortLinkForm
from django.views.generic.edit import FormView
from .models import *
from django.db.models import ObjectDoesNotExist


class MainView(FormView):
    """View for main page
        Renders main page of application that contains form for short link creation"""
    template_name = 'linkapp/main.html'  # Template used for this view
    form_class = ShortLinkForm  # Form to render on page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        return context

    def form_valid(self, form):
        link = form.cleaned_data['link']  # Get content of form
        try:  # Try to fing existing link with given URL
            link_exist = ShortLink.objects.all().get(full_link=ShortLink.check_full_link(link))
        except Exception as e:
            link_exist = None
        if not link_exist:  # If link is unique
            new_link = ShortLink(full_link=link, redirects=0)  # Create new ShortLink model
            new_link.save()
            new_link.generate_shortened_link().save(force_update=True)  # Generate short link for it
            return redirect(new_link)  # Redirect to result page
        else:   # If not
            return redirect(link_exist)  # Return existing link URL


def result(request, link_id):
    """View for result page
        Renders result page with short link for user's link"""
    link = None
    error = False
    try:  # Get URI of link
        link = request.build_absolute_uri(ShortLink.objects.get(id=link_id).shortened_link)
    except ObjectDoesNotExist as e:
        error = True  # If link with such ID is not exist return error
    return render(request, 'linkapp/result.html', context={'link': link, 'error': error})


def redirect_view(request, short_link):
    """View for redirecting to full link"""
    link = ShortLink.objects.get(shortened_link__contains=short_link)  # Find given link model
    link.increment_redirects()  # Increment it's redirects counter
    link.save(force_update=True)  # Save changes to DB
    link = link.full_link  # Get link's full URL
    return HttpResponseRedirect(str(link))  # Send redirect to it


def list_view(request):
    """View for list of all short links"""
    link_list = ShortLink.objects.all().order_by('-redirects')  # Get all links ordered by their redirects
    paginator = Paginator(link_list, 3)  # Create paginator with 10 links on page
    page_number = request.GET.get('page')  # Get page number fro request if exist
    page_obj = paginator.get_page(page_number)  # Get one page fro paginator
    context = {'page_obj': page_obj}  # Write page to context
    return render(request, 'linkapp/list.html', context=context)
