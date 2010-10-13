from django.conf.urls.defaults import *
from rangedogs.rangereport.models import *
import random
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'}),

    (r'^reports/$', 'django.views.generic.list_detail.object_list', {'queryset': Report.objects.all(), 'paginate_by': 25, 'template_object_name': 'reports'}),
    (r'^report/add/$', 'rangedogs.rangereport.views.smart_create', {'model': Report, 'login_required': True}),
    (r'^report/edit/(?P<object_id>\d+)/$', 'rangedogs.rangereport.views.limited_update', {'model': Report, 'login_required': True}),
    (r'^report/delete/(?P<object_id>\d+)/$', 'rangedogs.rangereport.views.limited_delete', {'model': Report, 'login_required': True}),
    (r'^report/(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', {'queryset': Report.objects.all(), 'template_object_name': 'report'}),
    (r'^report/random/$', 'django.views.generic.list_detail.object_detail', {'queryset': Report.objects.all(), 'object_id': random.randint(0, Report.objects.count()), 'template_object_name': 'report'}),

    (r'^calibers/$', 'django.views.generic.list_detail.object_list', {'queryset': Caliber.objects.all(), 'template_object_name': 'calibers'}),
    (r'^caliber/(?P<slug>[a-z0-9_-]+)/handloads/$', 'rangedogs.rangereport.views.limited_list', {'model': Handload, 'restrict_field': 'caliber__slug', 'template_object_name': 'caliber', 'extra_context': {'add_title': 'caliber'}}),
    (r'^caliber/(?P<slug>[a-z0-9_-]+)/guns/$', 'rangedogs.rangereport.views.limited_list', {'model': Gun, 'restrict_field': 'caliber__slug', 'template_object_name': 'caliber', 'extra_context': {'add_title': 'caliber'}}),
    (r'^caliber/(?P<slug>[a-z0-9_-]+)/$', 'django.views.generic.list_detail.object_detail', {'queryset': Caliber.objects.all(), 'template_object_name': 'caliber'}),

    (r'^handload/add/$', 'rangedogs.rangereport.views.smart_create', {'model': Handload, 'login_required': True}),
    (r'^handload/edit/(?P<object_id>\d+)/$', 'rangedogs.rangereport.views.limited_update', {'model': Handload, 'login_required': True}),
    (r'^handload/delete/(?P<object_id>\d+)/$', 'rangedogs.rangereport.views.limited_delete', {'model': Handload, 'login_required': True}),
    (r'^handload/(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', {'queryset': Handload.objects.all(), 'template_object_name': 'handload'}),

    (r'^gun/add/$', 'rangedogs.rangereport.views.smart_create', {'model': Gun, 'login_required': True}),
    (r'^gun/edit/(?P<object_id>\d+)/$', 'rangedogs.rangereport.views.limited_update', {'model': Gun, 'login_required': True}),
    (r'^gun/delete/(?P<object_id>\d+)/$' 'rangedogs.rangereport.views.limited_delete', {'model': Gun, 'login_required': True}),
    (r'^gun/(?P<object_id>\d+)/', 'django.views.generic.list_detail.object_detail', {'queryset': Gun.objects.all(), 'template_object_name': 'gun'}),

    (r'^comment/$', 'rangedogs.rangereport.views.post_comment'),
    (r'^comment/edit/(?P<object_id>\d+)/$', 'rangedogs.rangereport.views.limited_update', {'model': Comment, 'login_required': True}),
    (r'^comment/delete/(?P<object_id>\d+)/$', 'rangedogs.rangereport.views.limited_delete', {'model': Comment, 'login_required': True}),

    (r'^user/(?P<slug>[a-zA-Z0-9_]+)/$', 'django.views.generic.list_detail.object_detail', {'queryset': User.objects.all(), 'slug_field': 'username', 'template_object_name': 'user_obj', 'template_name': 'registration/profile.html'}),
    (r'^user/(?P<slug>[a-zA-Z0-9_]+)/reports/$', 'rangedogs.rangereport.views.limited_list', {'model': Report, 'restrict_field': 'owner__username', 'paginate_by': 25, 'template_object_name': 'reports', 'extra_context': {'add_title': 'user'}}),
    (r'^user/(?P<slug>[a-zA-Z0-9_]+)/guns/$', 'rangedogs.rangereport.views.limited_list', {'model': Gun, 'restrict_field': 'owner__username', 'paginate_by': 100, 'template_object_name': 'guns', 'extra_context': {'add_title': 'user'}}),
    (r'^user/(?P<slug>[a-zA-Z0-9_]+)/handloads/$', 'rangedogs.rangereport.views.limited_list', {'model': Handload, 'restrict_field': 'owner__username', 'paginate_by': 100, 'template_object_name': 'handloads', 'extra_context': {'add_title': 'user'}}),

    #(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    #(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    #(r'^accounts/create/$', 'rangedogs.rangereport.views.user_create'),
    (r'^accounts/profile/$', 'rangedogs.rangereport.views.user_home'),
    (r'^accounts/profile/edit/$', 'rangedogs.rangereport.views.user_edit'),
    #(r'^accounts/password/change/$', 'django.contrib.auth.views.password_change'),
    #(r'^accounts/password/change/done/$', 'django.contrib.auth.views.password_change_done'),
    #(r'^accounts/password/reset/$', 'django.contrib.auth.views.password_reset'),
    #(r'^accounts/password/reset/done/$', 'django.contrib.auth.views.password_reset_done')
    (r'^accounts/', include('registration.urls')),

    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
)
