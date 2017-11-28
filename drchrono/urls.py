from django.conf.urls import include, url
from django.views.generic import TemplateView

from . import views


urlpatterns = [
    url(r'^$', views.Home.as_view(), name='home'),
    url(r'^appt$', views.Appt.as_view(), name='appt'),
    url(r'^p_login/(\d+)/(\d+)$', views.PatientCheckin.as_view(), name='p_login'),
    url(r'^demographic/(\d+)/(\d+)$', views.Demographics.as_view(), name='demog'),
    url(r'^checkin/(\d+)$', views.Checkin.as_view(), name='checkin'),
    url(r'^d_waitlist$', views.Waitlist.as_view(), name='d_waitlist'),
    url(r'^begin$', TemplateView.as_view(template_name='begin.html'), name='begin'),
    url(r'^d_login$', TemplateView.as_view(template_name='doctor_login.html'), name='d_login'),
    url(r'^logout$', views.Logout.as_view(), name='logout'),

    url(r'', include('social.apps.django_app.urls', namespace='social')),

    # included to provide easy access to checkin error page
    # url(r'^checkin_err$', TemplateView.as_view(template_name='checkin_error.html'), name='checkin_err'),
]
