from django.conf.urls import patterns, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from testsuite_app.views import *
from django.contrib.auth.decorators import login_required
from . import settings

admin.autodiscover()


"""

scheme

note that in some cases, IDs are numbers and in other cases, human-readable identifiers.

/ : landing page

/testsuite/<id>/ : evaluations for testsuite (e.g. 'reading systems' page or 'accessibility' page)
/testsuite/<id>/archive/: archived evaluations for testsuite

/evaluation/<id>/ : single reading system results for one testsuite 
/testsuite/<id>/feature/<id>: many reading system results for one feature
/testsuite/: instructions and downloads
/docs/*: static pages with instructions etc

ACTIONS for logged-in users (permissions vary for each action):
/manage/: logged-in user starting point
/rs/add/: add new reading system
/rs/<id>/edit/: edit reading system
/rs/<id>/delete/: delete reading system
/rs/<id>/testsuite/<id>/add/: add evaluation for reading system + testsuite
/evaluation/<id>/edit/: edit evaluation overview
/evaluation/<id>/edit/section/<id>/: edit evaluation section
/evaluation/<id>/delete/: delete evaluation
/evaluation/<id>/(un)publish/: publish/unpublish evaluation
/evaluation/<id>/(un)archive/: archive/unarchive evaluation
/rs/all/ : view all reading systems
/evaluation/all/: view all evaluations

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
    # url order is important because of the human-readable IDs (i.e any character allowed, any length)
    (r'^testsuite/(?P<testsuite_id>.+)/feature/(?P<feature_id>.+)/$', FeatureView.as_view()),
    (r'^testsuite/(?P<testsuite_id>.+)/archive/$', ArchiveGridView.as_view()),
    (r'^testsuite/(?P<testsuite_id>.+)/$', GridView.as_view()),
    
    
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
    (r'^evaluation/(?P<pk>\d+)/edit/section/(?P<epub_id>.*)/$', login_required(function=EditEvaluationSingleEpubView.as_view(), login_url='/login/')),


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
