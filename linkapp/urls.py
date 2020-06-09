from django.conf.urls import url
from . import views

app_name = 'linker'
# URL patterns used in Linker app
urlpatterns = [
url(r'^$', views.MainView.as_view(), name='main'),  # Main page URL
url(r'^list/$', views.list_view, name='list'),  # List of all links page URL
url(r'^(?P<link_id>\d+)/result/$', views.result, name='result'),  # Short link creation result page URL
url(r'^(?P<short_link>.*)/$', views.redirect_view, name='redirect_view'),  # Redirect to full link URL
]