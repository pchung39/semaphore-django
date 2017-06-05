from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.lander, name='lander'),
    url(r'^signin/', views.signin, name='signin'),
    url(r'^signup/', views.signup, name='signup'),
    #url(r'^service/', views.select_instance, name='select_instance'),
    url(r'^manage/', views.manage_services, name='manage'),
    url(r'^delete/(?P<instance_id>[0-9]+)/$', views.delete_instance, name='delete_instance'),

]
