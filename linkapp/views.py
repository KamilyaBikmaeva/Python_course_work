from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ShortLinkForm
from django.views.generic.edit import FormView
from .models import *
from django.db.models import ObjectDoesNotExist


class MainView(FormView):
    template_name = 'linkapp/main.html'
    form_class = ShortLinkForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        return context

    def form_valid(self, form):
        link = form.cleaned_data['link']
        try:
            link_exist = ShortLink.objects.all().get(full_link=ShortLink.check_full_link(link))
        except Exception as e:
            link_exist = None
        if not link_exist:
            new_link = ShortLink(full_link=link, redirects=0)
            new_link.save()
            new_link.generate_shortened_link().save(force_update=True)
            return redirect(new_link)
        else:
            return redirect(link_exist)


def result(request, link_id):
    link = None
    error = False
    try:
        link = request.build_absolute_uri(ShortLink.objects.get(id=link_id).shortened_link)
    except ObjectDoesNotExist as e:
        error = True
    return render(request, 'linkapp/result.html', context={'link': link, 'error': error})


def redirect_view(request, short_link):
    link = ShortLink.objects.get(shortened_link__contains=short_link)
    link.increment_redirects()
    link.save(force_update=True)
    link = link.full_link
    return HttpResponseRedirect(str(link))


def list_view(request):
    link_list = ShortLink.objects.all().order_by('-redirects')
    paginator = Paginator(link_list, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'linkapp/list.html', context=context)
