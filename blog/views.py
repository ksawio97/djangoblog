from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .forms import PostForm
from django.views.generic import DetailView, TemplateView
from datetime import datetime

class Image(TemplateView):
    form = PostForm
    template_name = 'blog/image.html'

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.Files)

        if form.is_valid():
            obj = form.save()
            return HttpResponseRedirect(reverse_lazy('image_display', kwargs={'pk': obj.id}))
        
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    
class ImageDisplay(DetailView):
    model = Post
    template_name = 'blog/image_display.html'
    context_object_name = 'image'


def post_list(request):
    posts = Post.objects.all().order_by('publish_date')

    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def error_404_view(request, exception):
    data = {"name": "Blog"}
    return render(request, 'blog/404.html')

def post_new(request):
    # not logged users can't add posts
    if not _isUserAuth(request):
        return redirect('/')
    
    if request.method != "POST":
        form = PostForm()
    else:
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.publish_date = datetime.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
        
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    # not logged users can't edit posts
    if not _isUserAuth(request):
        return redirect('/')

    post = get_object_or_404(Post, pk=pk)
    if request.method != "POST":
        form = PostForm(instance=post)
    else:
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.publish_date = datetime.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
        
    return render(request, 'blog/post_edit.html', {'form': form})

def _isUserAuth(request) -> bool:
    return request.user.is_authenticated 