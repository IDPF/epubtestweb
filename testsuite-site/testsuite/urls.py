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
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    (r'^auth/$', auth_and_login),
    (r'^logout/$', logout_user),
    (r'^manage/$', login_required(function=ManageView.as_view(), login_url='/login/')),
    #(r'^new_evaluation/$', login_required(function=CreateNewEvaluationView.as_view(), login_url='/login/')),
    (r'^rs/(?P<pk>\d+)/$', ReadingSystemView.as_view()),
    (r'^rs/(?P<pk>\d+)/edit$', login_required(function=EditEvaluationView.as_view(), login_url='/login/')),
    # (r'^confirm_delete_rs/$', login_required(function=ConfirmDeleteRSView.as_view(), login_url='/login/')),
    # (r'^delete_rs/$', login_required(delete_rs, login_url='/login/')),
    # (r'^confirm_delete_ev/$', login_required(function=ConfirmDeleteEvalView.as_view(), login_url='/login/')),
    # (r'^delete_ev/$', login_required(delete_ev, login_url='/login/')),
    (r'^rs/new$', login_required(function=NewReadingSystemView.as_view(), login_url='/login/')),
    #(r'^edit_rs/(?P<pk>\d+)/$', login_required(function=EditReadingSystemView.as_view(), login_url='/login/')),
    (r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
