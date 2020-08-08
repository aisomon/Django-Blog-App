from django.shortcuts import render, get_object_or_404, redirect,Http404
from .models import Author,Category,Article,Comment
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import createForm, registerUser,createAuthor,commentForm,createCategoryForm
from django.contrib import messages

# Create your views here.
def home(request):
    post = Article.objects.all()
    search = request.GET.get('q') # receving the searching word
    if search:
        post=post.filter(
            Q(title__icontains=search) | 
            Q(body__icontains=search)
        )
    paginator = Paginator(post, 8) # Show 8 contacts per page.
    page_number = request.GET.get('page')
    total_article = paginator.get_page(page_number)
    context = {
        "post" : total_article
    }
    return render(request,'index.html', context)

def getauthor(request, name):
    post_author = get_object_or_404(User, username=name)
    auth = get_object_or_404(Author,name=post_author.id)
    post = Article.objects.filter(article_author=auth.id)
    contex = {
        "auth":auth,
        "post":post
    }
    return render(request, "profile.html" ,contex)

def getsingle(request, id):
    post = get_object_or_404(Article, pk = id)
    first = Article.objects.first()
    last = Article.objects.last()
    getComment=Comment.objects.filter(post=id)
    related = Article.objects.filter(category=post.category).exclude(id=id)[:4]
    form=commentForm(request.POST or None)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.post=post
        instance.save()
        messages.success(request,'Comment is successfully added.')

    context = {
        "post" : post,
        "first" : first,
        "last" : last,
        "related" : related,
        "form" : form,
        "comment" : getComment
    }
    return render(request,'single.html', context)

def getTopic(request, name):
    cat = get_object_or_404(Category, name = name)
    post = Article.objects.filter(category=cat.id)
    return render(request,'category.html',{"post":post, "cat": cat})

def getLogin(request):            
    if request.user.is_authenticated:
        return redirect('blog:index')
    else:
        if request.method=="POST":
            user=request.POST.get('user')
            password = request.POST.get('pass')
            auth = authenticate(request, username=user, password =password)
            if auth is not None:
                login(request,auth)
                return redirect('blog:index')
            else:
                messages.add_message(request, messages.ERROR, 'Username or password mismatch!')
    return render(request,'login.html')


def getLogout(request):
    logout(request)
    return redirect('blog:index')

def getCreate(request):
    if request.user.is_authenticated:
        u=get_object_or_404(Author,name=request.user.id)
        form = createForm(request.POST or None , request.FILES or None) # here request.Files for Image file
        if form.is_valid():
            instance=form.save(commit=False)
            instance.article_author=u
            instance.save()
            messages.success(request,'Article is posted successfully.')
            return redirect('blog:index')
        return render(request,'create.html', { 'form':form })
    else:
        return redirect('blog:login')

def getProfile(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=request.user.id)
        author_profile = Author.objects.filter(name=user.id)
        if author_profile:
            authorUser = get_object_or_404(Author, name=request.user.id)
            post = Article.objects.filter(article_author=authorUser.id)
            return render(request, 'logged_in_profile.html', {"post": post, "user": authorUser})
        else:
            form =createAuthor(request.POST or None, request.FILES or None)
            if form.is_valid():
                instance=form.save(commit=False)
                instance.name=user
                instance.save()
                messages.success(request, 'Author profile is created successfully')
                return redirect('blog:profile')
            return render(request, 'createAuthor.html', {"form": form})

    else:
        return redirect('blog:login')



def getUpdate(request,pid):
    if request.user.is_authenticated:
        u=get_object_or_404(Author,name=request.user.id)
        post=get_object_or_404(Article,id=pid) # this is for getting all values in updated form
        form = createForm(request.POST or None , request.FILES or None, instance=post) # here request.Files for Image file, and instance=post means i am giving all values of instance
        if form.is_valid():
            instance=form.save(commit=False)
            instance.article_author=u
            instance.save()
            messages.add_message(request, messages.SUCCESS, 'Post updated successfully.')
            return redirect('blog:profile')
        return render(request,'create.html', { 'form':form })
    else:
        return redirect('blog:login')

def getDelete(request,pid):
    if request.user.is_authenticated:
        post=get_object_or_404(Article,id=pid) # this is for getting all values in updated form
        post.delete()
        messages.add_message(request, messages.WARNING, 'Post deleted successfully.')
        return redirect('blog:profile')
    else:
        return redirect('blog:login')

def getRegister(request):
    form=registerUser(request.POST or None)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.save()
        messages.success(request,'Registration sucessfully completed.')
        return redirect('blog:login')
    return render(request,'register.html',{"form":form})

def getCategory(request):
    query=Category.objects.all()
    return render(request,'topics.html',{"topic":query})

def getCreateCategory(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            form=createCategoryForm(request.POST or None)
            if form.is_valid():
                inatance=form.save(commit=False)
                inatance.save()
                messages.success(request,"Topic is created!")
                return redirect('blog:category')
            return render(request,'createCategory.html',{"form":form})
        else:
            raise Http404('You are not authorize to access this page!')
    else:
        return redirect('blog:login')