from django.shortcuts import render, redirect, get_object_or_404
# from django.http import HttpResponse
from .models import PostModel
from .forms import PostModelForm, PostUpdateForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# from django.core.paginator import Paginator

@login_required
def index(request):
    posts = PostModel.objects.all()
    if request.method == 'POST':
        form = PostModelForm(request.POST, request.FILES)
        if form.is_valid():
            for i in form:
                print(i)
            instance = form.save(commit=False)
            # instance.image = request.POST.get['image']
            instance.image = request.FILES.get('image', None)
            instance.author = request.user
            instance.save()
            redirect_url = reverse('index-home') + f'?post_id={instance.id}'
            return redirect(redirect_url)
        else:
    
            print(form.errors)
    else:
        form = PostModelForm()
    context = {
        "posts":posts,
        "form":form,
    }
    return render(request,'index.html',context)

@login_required
def post_details(request, pk):
    post = PostModel.objects.get(id=pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.user = request.user
            instance.post = post
            instance.save()
            redirect('post-details', pk=post.id)
    else:
        comment_form = CommentForm()
    context = {
        'post':post,
        'comment_form': comment_form
    }
    return render(request, 'post_details.html', context)

@login_required
def post_edit(request, pk):
    post = PostModel.objects.get(id=pk)
    if request.method == 'POST':
        form = PostUpdateForm(request.POST, instance=post)
        if form.is_valid():
           form.save()
           return redirect('index-home')
    else:
        form = PostUpdateForm(instance=post)
    context = {
        'post':post,
        'form':form,
    }
    return render(request, 'post_edit.html', context)

@login_required
def post_delete(request, pk):
        post = get_object_or_404(PostModel, id=pk)
        post.delete()
        return redirect('index-home') 


# def post_list(request):
#     post_list = PostModel.objects.all()
#     paginator = Paginator(post_list, 5) 

#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'index.html', {'page_obj': page_obj})

