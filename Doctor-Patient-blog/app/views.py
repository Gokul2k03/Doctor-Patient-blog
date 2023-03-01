from unicodedata import category
from django.shortcuts import render, redirect
from .forms import UserRegister, LoginForm, BlogCreation
from . models import User, Blog
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib import messages


def home(request):
    return render(request, 'home.html')


def register_doc(request):
    if request.method == 'POST':
        form = UserRegister(request.POST, request.FILES)
        if form.is_valid():
            ref_id = form.cleaned_data['username']
            form.save()
            c = User.objects.get(Q(username=ref_id))
            print(c)
            c.is_doctor = True
            if(len(request.FILES) != 0):
                c.profile_pic = request.FILES['image']
            c.save()
            messages.success(
                request, 'You(Doctor) have registered successfully. Login In Now')
            return redirect('login')
        else:
            msg = 'Errors while validating the form. Try Again!'
            return render(request, 'register.html', {'form': form, 'msg': msg})
    else:
        form = UserRegister()
        return render(request, 'register.html', {'form': form})


def register_pat(request):
    if request.method == 'POST':
        form = UserRegister(request.POST, request.FILES)
        if form.is_valid():
            ref_id = form.cleaned_data['username']
            form.save()
            c = User.objects.get(Q(username=ref_id))
            print(c)
            c.is_patient = True
            if(len(request.FILES) != 0):
                c.profile_pic = request.FILES['image']
            c.save()
            messages.success(
                request, 'You(Patient) have registered successfully. Login In Now')
            return redirect('login')
        else:
            msg = 'Errors while validating the form. Try Again!'
            return render(request, 'registerpat.html', {'form': form, 'msg': msg})
    else:
        form = UserRegister()
        return render(request, 'registerpat.html', {'form': form})


def login(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_doctor is True:
                data = Blog.objects.filter(is_draft=False)
                auth_login(request, user)
                return render(request, 'blogs.html', {'data': data})
            elif user is not None and user.is_doctor is False:
                data = Blog.objects.filter(is_draft=False)
                auth_login(request, user)
                return render(request, 'blogs.html', {'data': data})
            else:
                msg = 'You have entered incorrect username or password'
                return render(request, 'login.html', {'form': form, 'msg': msg})
        else:
            msg = 'Error has occured. Try Again'
    return render(request, 'login.html', {'form': form, 'msg': msg})


def blogs(request):
    data = Blog.objects.filter(is_draft=False)
    return render(request, 'blogs.html', {'data': data})


def drafts(request):
    data = Blog.objects.filter(is_draft=True, user=request.user)
    return render(request, 'drafts.html', {'data': data})


def myblogs(request):
    data = Blog.objects.filter(user=request.user, is_draft=False)
    return render(request, 'myblogs.html', {'data': data})


def createBlog(request):
    if request.method == 'POST':
        form = BlogCreation(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            user = request.user
            blog_category = form.cleaned_data['blog_category']
            summary = form.cleaned_data['summary']
            content = form.cleaned_data['content']
            is_draft = form.cleaned_data['is_draft']
            blog = Blog(
                user=user, title=title, blog_category=blog_category, summary=summary, content=content, is_draft=is_draft)
            blog.save()
            c = Blog.objects.get(Q(user=request.user) & Q(title=title))
            c.user = user
            if(len(request.FILES) != 0):
                c.blog_image = request.FILES['image']
            c.save()
            if(is_draft == False):
                messages.success(
                    request, 'Your Blog has been Successfully Created')
                return redirect('myblogs')
            else:
                messages.success(
                    request, 'Your Draft has been Successfully Created')
                return redirect('drafts')
        else:
            msg = 'Try Again!'
            return render(request, 'createblog.html', {'form': form, 'msg': msg})
    else:
        form = BlogCreation()
        return render(request, 'createblog.html', {'form': form})


def blogsall(request):
    data = Blog.objects.filter(is_draft=False)
    return render(request, 'blogs.html', {'data': data})


def mhealth(request):
    data = Blog.objects.filter(is_draft=False, blog_category='Mental Health')
    return render(request, 'blogs.html', {'data': data})


def heartdis(request):
    data = Blog.objects.filter(is_draft=False, blog_category='Heart Disease')
    return render(request, 'blogs.html', {'data': data})


def covid19(request):
    data = Blog.objects.filter(is_draft=False, blog_category='COVID19')
    return render(request, 'blogs.html', {'data': data})


def immun(request):
    data = Blog.objects.filter(is_draft=False, blog_category='Immunization')
    return render(request, 'blogs.html', {'data': data})
