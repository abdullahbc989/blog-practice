from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
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
    queryset = Post.objects.all()
    context = {
        "object_list": queryset,
    }
    template = "post_list.html"
    return render(request, template, context)


def post_detail(request, id=None):
    instance = get_object_or_404(Post, id=id)
    template = "post_detail.html"
    context = {
        "instance": instance
    }
    return render(request, template, context)


def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()

    template = "post_create.html"
    context = {
        "form": form,
    }
    return render(request, template, context)


def post_update(request):
    return HttpResponse("Update")


def post_delete(request):
    return HttpResponse("Delete")
