from django.conf.urls.defaults import patterns

urlpatterns = patterns('django.views.generic',
    (r'^$', 'simple.direct_to_template', {'template': 'base.html'}),
)
