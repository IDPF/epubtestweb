from django.conf.urls import patterns, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from testsuite_app.views import *
from django.contrib.auth.decorators import login_required
from . import settings

admin.autodiscover()


"""

URL ideas

/ : landing page

/testsuite/ID : evaluations for testsuite (e.g. 'reading systems' page or 'accessibility' page)
/testsuite/ID/archive: archived evaluations for testsuite

/evaluation/ID : single reading system results for one testsuite 
/testsuite/ID/feature/ID: many reading system results for one feature
/testsuite: instructions and downloads
/docs: static pages with instructions etc

ACTIONS for logged-in users (permissions vary for each action):
/manage: logged-in user starting point
/rs/add: add new reading system
/rs/ID/edit: edit reading system
/rs/ID/delete: delete reading system
/rs/ID/testsuite/ID/add: add evaluation for reading system + testsuite
/evaluation/ID/edit: edit evaluation
/evaluation/ID/delete: delete evaluation
/evaluation/ID/publish: publish/unpublish evaluation
/rs/all : view all reading systems
/evaluation/all: view all evaluations

"""

urlpatterns = patterns('',
    # static pages
    (r'^$', IndexView.as_view()),
    (r'^docs/instructions-for-evaluators/$', InstructionsForEvaluatorsView.as_view()),
    (r'^docs/instructions-for-accessibility-evaluators/$', InstructionsForAccessibilityEvaluatorsView.as_view()),
    (r'^docs/call-for-moderators/$', CallForModeratorsView.as_view()),    
    (r'^testsuite/$', TestsuiteView.as_view()),
    
    # public reports
    (r'^features/$', FeaturesView.as_view()),
    (r'^testsuite/(?P<testsuite_id>.*)/$', GridView.as_view()),
    (r'^testsuite/(?P<testsuite_id>.*)/features/(?P<feature_id>.*)$', FeatureView.as_view()),
    (r'^evaluation/(?P<pk>\d+)/$', EvaluationView.as_view()),

    
    # (r'^archived-results/$', ArchivedResultsView.as_view()),
    
    # authorization    
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    (r'^auth/$', auth_and_login),
    (r'^logout/$', logout_user),
    
    # pages for logged-in users
    (r'^manage/$', login_required(function=ManageView.as_view(), login_url='/login/')),

    (r'^rs/add/$', login_required(function=AddEditReadingSystemView.as_view(), login_url='/login/')),
    (r'^rs/(?P<pk>\d+)/edit/$', login_required(function=AddEditReadingSystemView.as_view(), login_url='/login/')),
    (r'^rs/(?P<pk>\d+)/delete/$', login_required(function=ConfirmDeleteReadingSystemView.as_view(), login_url='/login/')),
    
    (r'^evaluation/add/$', login_required(function=AddEvaluationView.as_view(), login_url='/login/')),
    (r'^evaluation/(?P<pk>\d+)/delete/$', login_required(function=ConfirmDeleteEvaluationView.as_view(), login_url='/login/')),
    (r'^evaluation/all/$', login_required(function=AllEvaluationsView.as_view(), login_url='/login/')),
    (r'^rs/all/$', login_required(function=AllReadingSystemsView.as_view(), login_url='/login/')),

    (r'^evaluation/(?P<pk>\d+)/publish/$', login_required(function=publish_evaluation, login_url='/login/')),
    (r'^evaluation/(?P<pk>\d+)/unpublish/$', login_required(function=unpublish_evaluation, login_url='/login/')),
    (r'^evaluation/(?P<pk>\d+)/archive/$', login_required(function=archive_evaluation, login_url='/login/')),
    (r'^evaluation/(?P<pk>\d+)/unarchive/$', login_required(function=unarchive_evaluation, login_url='/login/')),
    (r'^evaluation/(?P<pk>\d+)/edit/$', login_required(function=EditEvaluationView.as_view(), login_url='/login/')),
    (r'^evaluation/(?P<pk>\d+)/edit/(?P<epub_id>.*)$', login_required(function=EditEvaluationView.as_view(), login_url='/login/')),

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
