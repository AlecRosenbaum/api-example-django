from django.conf.urls import include, url
from django.views.generic import TemplateView

from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^appt$', views.appt, name='appt'),
    url(r'^p_login/(\d+)/(\d+)$', views.patient_checkin, name='p_login'),
    url(r'^demographic/(\d+)/(\d+)$', views.demographics, name='demog'),
    url(r'^checkin/(\d+)$', views.check_in, name='checkin'),
    url(r'^d_waitlist$', views.waitlist, name='d_waitlist'),
    url(r'^begin$', TemplateView.as_view(template_name='begin.html'), name='begin'),


    # url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    # url(r'^checkin$', TemplateView.as_view(template_name='checkin.html'), name='checkin'),
    # url(r'^d_waitlist$', TemplateView.as_view(template_name='d_waitlist.html'), name='d_waitlist'),
    url(r'^d_login$', TemplateView.as_view(template_name='doctor_login.html'), name='d_login'),
    url(r'^d_logout$', TemplateView.as_view(template_name='doctor_logout.html'), name='d_logout'),

    url(r'^logout$', views.logout, name='logout'),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
]
