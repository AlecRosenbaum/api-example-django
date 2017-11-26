from django.conf.urls import include, url
from django.views.generic import TemplateView

from . import views


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^begin$', TemplateView.as_view(template_name='begin.html'), name='begin'),
    url(r'^p_login$', views.patient_checkin, name='p_login'),
    
    # url(r'^p_login$', TemplateView.as_view(template_name='patient_login.html'), name='p_login'),
    url(r'^demographic$', TemplateView.as_view(template_name='demographic.html'), name='demog'),
    url(r'^checkin$', TemplateView.as_view(template_name='checkin.html'), name='checkin'),
    url(r'^d_login$', TemplateView.as_view(template_name='doctor_login.html'), name='d_login'),
    url(r'^d_logout$', TemplateView.as_view(template_name='doctor_logout.html'), name='d_logout'),
    url(r'^d_waitlist$', TemplateView.as_view(template_name='d_waitlist.html'), name='d_waitlist'),

    url(r'', include('social.apps.django_app.urls', namespace='social')),
]
