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
/grid : evaluations  
/grid/archive: archived evaluations
/grid/ID/testsuite/ID : single reading system results for one testsuite 
/testsuite/ID/feature/ID: many reading system results for one feature
/accessibility: accessibility evaluations
/accessibility/archive: archived accessibility evaluations


/manage: logged-in user starting point

/docs: static pages with instructions etc


"""

urlpatterns = patterns('',
    (r'^$', IndexView.as_view()),
    (r'^features/$', FeaturesView.as_view()),
    (r'^grid/$', GridView.as_view()),
    (r'^accessibility/$', AccessibilityGridView.as_view()),
    (r'^testsuite/(?P<testsuite_id>.*)/features/(?P<feature_id>.*)$', FeatureView.as_view()),
    (r'^grid/(?P<pk>\d+)/testsuite/(?P<testsuite_id>.*)$', ReadingSystemView.as_view()),
    (r'^docs/instructions-for-evaluators/$', InstructionsForEvaluatorsView.as_view()),
    (r'^docs/instructions-for-accessibility-evaluators/$', InstructionsForAccessibilityEvaluatorsView.as_view()),
    (r'^docs/call-for-moderators/$', CallForModeratorsView.as_view()),    
    
    (r'^testsuite/$', TestsuiteView.as_view()),

    
    # (r'^archived-results/$', ArchivedResultsView.as_view()),
    
    
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    (r'^auth/$', auth_and_login),
    (r'^logout/$', logout_user),
    
    (r'^manage/$', login_required(function=ManageView.as_view(), login_url='/login/')),
    
    # (r'^rs/(?P<pk>\d+)/accessibility/$', AccessibilityConfigurationsView.as_view()),
    # (r'^rs/(?P<pk>\d+)/accessibility/(?P<rset>\d+)$', AccessibilityReadingSystemView.as_view()),
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
