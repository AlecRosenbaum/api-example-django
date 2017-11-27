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
    url(r'^d_login$', TemplateView.as_view(template_name='doctor_login.html'), name='d_login'),
    url(r'^logout$', views.logout, name='logout'),

    url(r'', include('social.apps.django_app.urls', namespace='social')),

    # included to provide easy access to checkin error page
    # url(r'^checkin_err$', TemplateView.as_view(template_name='checkin_error.html'), name='checkin_err'),
]
