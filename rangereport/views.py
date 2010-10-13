from rangedogs.rangereport.models import *
from rangedogs.rangereport.forms import *
from django.views.generic.create_update import *
from django.views.generic.list_detail import object_list
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required

@login_required
def limited_update(request, **kwargs):
    if (request.user.username == lookup_object(kwargs['model'], kwargs['object_id'], kwargs['slug'], kwargs['slug_field']).owner.username):
        return update_object(request, **kwargs)

@login_required
def limited_delete(request, **kwargs):
    if (request.user.username == lookup_object(kwargs['model'], kwargs['object_id'], kwargs['slug'], kwargs['slug_field']).owner.username):
        return delete_object(request, **kwargs)

@login_required
def smart_create(request, **kwargs):
    if (request.method == "POST"):
        request.POST = request.POST.copy()
        request.POST.__setitem__('owner', str(request.user.id))
    return create_object(request, **kwargs)

def limited_list(request, slug = None, model = None, restrict_field = None, paginate_by = None, template_object_name = None, extra_context = {}):
    query = model.objects.filter(**{str(restrict_field): str(slug)})
    extra_context['slug'] = slug
    return object_list(request, queryset = query, paginate_by = paginate_by, template_object_name = template_object_name, extra_context = extra_context)

def user_home(request):
    return render_to_response("registration/profile.html", {'user': request.user, 'profile': request.user.get_profile()})

def user_edit(request):
    if (request.method == "POST"):
        if (request.user.userprofile_set.count()):
            form = UserProfileForm(request.POST, instance=request.user.get_profile())
        else:
            form = UserProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit = False)
            profile.user = request.user
            profile.save
            form.save_m2m()
            profile.save()
            request.user.message_set.create(message="Information successfully updated!")
            return HttpResponseRedirect('/accounts/profile/')
    else:
        if (request.user.userprofile_set.count()):
            profile = UserProfileForm(instance=request.user.get_profile())
        else:
            profile = UserProfileForm()
        return render_to_response("registration/profile_form.html", {'form': profile})

def post_comment(request):
    form = request.POST
    if form.is_valid():
        if (form.cleaned_data['parent'] == 'User'):
            obj = get_object_or_404(User, pk=form.cleaned_data['object_id'])
            Comment.objects.create(
                    owner = request.user,
                    User_parent = obj,
                    title = form.cleaned_data['title'],
                    body = form.cleaned_data['body']
                    )
            return HttpRedirectResponse(request.GET['next'])
        elif (form.cleaned_data['parent'] == 'Gun'):
            obj = get_object_or_404(Gun, pk=form.cleaned_data['object_id'])
            Comment.objects.create(
                    owner = request.user,
                    Gun_parent = obj,
                    title = form.cleaned_data['title'],
                    body = form.cleaned_data['body']
                    )
            return HttpRedirectResponse(request.GET['next'])
        elif (form.cleaned_data['parent'] == 'Handload'):
            obj = get_object_or_404(Handload, pk=form.cleaned_data['object_id'])
            Comment.objects.create(
                    owner = request.user,
                    Handload_parent = obj,
                    title = form.cleaned_data['title'],
                    body = form.cleaned_data['body']
                    )
            return HttpRedirectResponse(request.GET['next'])
        elif (form.cleaned_data['parent'] == 'Report'):
            obj = get_object_or_404(Report, pk=form.cleaned_data['object_id'])
            Comment.objects.create(
                    owner = request.user,
                    Report_parent = obj,
                    title = form.cleaned_data['title'],
                    body = form.cleaned_data['body']
                    )
            return HttpRedirectResponse(request.GET['next'])
        elif (form.cleaned_data['parent'] == 'Comment'):
            obj = get_object_or_404(Comment, pk=form.cleaned_data['object_id'])
            Comment.objects.create(
                    owner = request.user,
                    Comment_parent = obj,
                    title = form.cleaned_data['title'],
                    body = form.cleaned_data['body']
                    )
            return HttpRedirectResponse(request.GET['next'])
