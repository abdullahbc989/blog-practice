from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
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
    queryset_list = Post.objects.all()  # .order_by("-
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
    }
    template = "post_list.html"
    return render(request, template, context)


def post_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    template = "post_detail.html"
    context = {
        "instance": instance
    }
    return render(request, template, context)


def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
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
    instance = get_object_or_404(Post, id=id)

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
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Deleted")
    return redirect("posts:home")
