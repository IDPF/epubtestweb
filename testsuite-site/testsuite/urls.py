from django.conf.urls import patterns, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from testsuite_app.views import *
from django.contrib.auth.decorators import login_required

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', IndexView.as_view()),
    (r'^about/$', AboutView.as_view()),
    (r'^testsuite/$', TestsuiteView.as_view()),
    (r'^compare/$', CompareResultsView.as_view()),
    (r'^results/$', CurrentResultsView.as_view()),
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    (r'^auth/$', auth_and_login),
    (r'^logout/$', logout_user),
    (r'^manage/$', login_required(function=ManageView.as_view(), login_url='/login/')),
    (r'^export/$', login_required(function=export_data_all, login_url='/login/')),
    (r'^rs/(?P<pk>\d+)/$', ReadingSystemView.as_view()),
    (r'^rs/(?P<pk>\d+)/export/$', login_required(function=export_data_single, login_url='/login/')),
    (r'^rs/(?P<pk>\d+)/edit/$', login_required(function=EditReadingSystemView.as_view(), login_url='/login/')),
    (r'^rs/(?P<pk>\d+)/eval/$', login_required(function=EditEvaluationView.as_view(), login_url='/login/')),
    (r'^rs/(?P<pk>\d+)/eval/(?P<cat>\d+)/$', login_required(function=EditEvaluationView.as_view(), login_url='/login/')),
    (r'^rs/(?P<pk>\d+)/delete/$', login_required(function=ConfirmDeleteRSView.as_view(), login_url='/login/')),
    (r'^rs/(?P<pk>\d+)/report/$', login_required(function=ProblemReportView.as_view(), login_url='/login/')),
    (r'^rs/new/$', login_required(function=EditReadingSystemView.as_view(), login_url='/login/')),
    (r'^rs/(?P<pk>\d+)/visibility/$', login_required(function=set_visibility, login_url='/login/')),
    (r'^admin/', include(admin.site.urls)),
    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.EPUB_URL, document_root = settings.EPUB_ROOT)
