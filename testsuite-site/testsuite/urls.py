from django.conf.urls import patterns, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from testsuite_app.views import *
from django.contrib.auth.decorators import login_required
from . import settings

admin.autodiscover()


"""
/ : landing page. list of all features for all testsuites
/rs : reading systems view (all reading systems)
/rs/ID/testsuiteID : reading system results for one testsuite
/ts/ID/feature/featureID: single feature view 
(maybe for the future)
/ts/ID/category/categoryID: single category view

"""

urlpatterns = patterns('',
    (r'^$', IndexView.as_view()),
    (r'^features/$', FeaturesView.as_view()),
    (r'^rs/$', ReadingSystemsView.as_view()),
    (r'^accessibility/$', AccessibleReadingSystemsView.as_view()),
    (r'^ts/(?P<pk>\d+)/features/(?P<feature_id>\d+)$', FeatureView.as_view()),
    (r'^rs/(?P<pk>\d+)/ts/(?P<testsuite_id>\d+)$', ReadingSystemView.as_view()),

    
    
    
    (r'^about/$', AboutView.as_view()),
    (r'^testsuite/$', TestsuiteView.as_view()),
    # (r'^results/$', CurrentResultsView.as_view()),
    # (r'^archived-results/$', ArchivedResultsView.as_view()),
    # (r'^call-for-moderators/$', CallForModeratorsView.as_view()),
    # (r'^testsuite-xml/$', gen_testsuite_xml),
    # (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    # (r'^auth/$', auth_and_login),
    # (r'^logout/$', logout_user),
    # (r'^manage/$', login_required(function=ManageView.as_view(), login_url='/login/')),
    # (r'^export/$', login_required(function=export_data_all, login_url='/login/')),
    
    # (r'^rs/(?P<pk>\d+)/accessibility/$', AccessibilityConfigurationsView.as_view()),
    # (r'^rs/(?P<pk>\d+)/accessibility/(?P<rset>\d+)$', AccessibilityReadingSystemView.as_view()),
    # (r'^rs/(?P<pk>\d+)/export/$', login_required(function=export_data_single, login_url='/login/')),
    # (r'^rs/(?P<pk>\d+)/edit/$', login_required(function=EditReadingSystemView.as_view(), login_url='/login/')),
    # (r'^rs/(?P<pk>\d+)/eval/$', login_required(function=EditResultSetView.as_view(), login_url='/login/')),
    # (r'^rs/(?P<pk>\d+)/eval/new$', login_required(function=EditResultSetView.as_view(), login_url='/login/')),
    # (r'^rs/(?P<pk>\d+)/eval/accessibility/$', login_required(function=EditAccessibilityConfigurationsView.as_view(), login_url='/login/')),
    # (r'^rs/(?P<pk>\d+)/eval/accessibility/new$', login_required(function=EditAccessibilityResultSetView.as_view(), login_url='/login/')),
    # (r'^rs/(?P<pk>\d+)/eval/accessibility/(?P<rset>\d+)$', login_required(function=EditAccessibilityResultSetView.as_view(), login_url='/login/')),
    # (r'^rs/(?P<pk>\d+)/accessibility/(?P<rset>\d+)/delete$', login_required(function=ConfirmDeleteAccessibilityConfigurationView.as_view(), login_url='/login/')),
    # (r'^rs/(?P<pk>\d+)/eval/(?P<cat>\d+)/$', login_required(function=EditResultSetView.as_view(), login_url='/login/')),
    # (r'^rs/(?P<pk>\d+)/delete/$', login_required(function=ConfirmDeleteRSView.as_view(), login_url='/login/')),
    # (r'^rs/(?P<pk>\d+)/report/$', login_required(function=ProblemReportView.as_view(), login_url='/login/')),
    # (r'^rs/new/$', login_required(function=EditReadingSystemView.as_view(), login_url='/login/')),
    # (r'^rs/(?P<pk>\d+)/archive/$', login_required(function=archive_rs, login_url='/login/')),
    # (r'^rs/(?P<pk>\d+)/unarchive/$', login_required(function=unarchive_rs, login_url='/login/')),
    # (r'^rs/(?P<pk>\d+)/visibility/$', login_required(function=set_rs_visibility, login_url='/login/')),
    # (r'^rs/(?P<pk>\d+)/accessibility/(?P<rset>\d+)/visibility/$', login_required(function=set_accessibility_visibility, login_url='/login/')),
    (r'^admin/', include(admin.site.urls)),
) 

additional_settings = patterns('',)

if settings.allow_robots == False:
    additional_settings = patterns('',
        (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain"))
    )

urlpatterns += additional_settings
    

urlpatterns = urlpatterns + \
static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.EPUB_URL, document_root = settings.EPUB_ROOT)
