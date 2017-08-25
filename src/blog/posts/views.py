from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.utils import timezone

from comments.models import Comment
from .models import Post
from .forms import PostForm

# Create your views here.


def post_list(request):
    # if request.user.is_authenticated():
    #    context = {

    #    }
    # else:
    #    context = {
    #
    #    }
    today = timezone.now().date()
    queryset_list = Post.objects.active()  # .order_by("-
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()  # no duplicates in search results
    paginator = Paginator(queryset_list, 5)

    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {
        "object_list": queryset,
        "today": today,
    }
    template = "post_list.html"
    return render(request, template, context)


def post_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    if instance.publish > timezone.now().date() or instance.draft:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    comments = instance.comments  # Comment.objects.filter_by_instance(instance)
    template = "post_detail.html"
    context = {
        "instance": instance,
        "comments": comments,
    }
    return render(request, template, context)


def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Created!")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Error in creation")

    template = "post_create.html"
    context = {
        "form": form,
    }
    return render(request, template, context)


def post_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)

    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Updated!")  # , extra_tags = ''
        return HttpResponseRedirect(instance.get_absolute_url())

    template = "post_create.html"
    context = {
        "instance": instance,
        "form": form,
    }
    return render(request, template, context)


def post_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Deleted")
    return redirect("posts:home")
