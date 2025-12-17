from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.urls import reverse
import logging
from .models import Category, Post, AboutUs
from django.http import Http404
from django.core.paginator import Paginator
from .forms import ContactForm, ForgotPasswordForm, LoginForm, PostForm, RegisterForm, ResetPasswordForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail

# Create your views here.

#posts = [{'id': 1, 'title': 'Post 1', 'content': 'This is the content of post 1.'},
#         {'id': 2, 'title': 'Post 2', 'content': 'This is the content of post 2.'},
#         {'id': 3, 'title': 'Post 3', 'content': 'This is the content of post 3.'},
#         {'id': 4, 'title': 'Post 4', 'content': 'This is the content of post 4.'}
#         ]


def index(request):
    blog_title = "Latest Posts"
    #getting data from post model 
    all_posts = Post.objects.all()
    #paginate
    paginator = Paginator(all_posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,'blog/index.html', {'blog_title': blog_title, 'page_obj': page_obj})

def detail(request, slug):  
    # posts = Post.objects.all()
     # post = next((item for item in posts if item['id'] == int(post_id)), None)
     #logger = logging.getLogger("TESTING")
     #logger.debug(f'Post variable is {post}')
     try:
         #getting data from post model by post_id
         post = Post.objects.get(slug=slug)
         related_posts = Post.objects.filter(category=post.category).exclude(pk=post.id)

     except Post.DoesNotExist:
         raise Http404("Post does not exist")
     
     return render(request,'blog/detail.html', {'post': post, 'related_posts': related_posts})

def old_url_redirect(request):
    return redirect(reverse('blog:new_page_url'))

def new_url_view(request):
    return HttpResponse("This is the new ID view.")

def contact_view(request):
     if request.method == "POST":
         form = ContactForm(request.POST)
         name = request.POST.get('name')
         email = request.POST.get('email')      
         message = request.POST.get('message')

         logger = logging.getLogger("TESTING")
         if form.is_valid():
            logger.debug(f'POST data is {form.cleaned_data['name']} {form.cleaned_data['email']} {form.cleaned_data['message']}')
            success_message = 'Your message has been sent successfully!'
            return render(request,'blog/contact.html', {'form': form, 'success_message': success_message})
         else:
             logger.debug("Form validation failed")
             return render(request,'blog/contact.html', {'form': form, 'name': name, 'email': email, 'message': message})
     return render(request,'blog/contact.html')

def about_view(request):
    about_content = AboutUs.objects.first()
    if about_content is None or not about_content.content:
        about_content = "Default about us content."
    else:
        about_content = about_content.content
    return render(request, 'blog/about.html',{'about_content': about_content})

def register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save( )
            messages.success(request, "Registration successful. You can now log in.") 
            return redirect("blog:login")  # Redirect to a success page.
    return render(request, 'blog/register.html', {'form': form})

def login(request):
    form = LoginForm()
    if request.method == "POST":
        #login form
        form = LoginForm(request.POST)
        if form.is_valid():
          username = form.cleaned_data['username']
          password = form.cleaned_data['password']
          user = authenticate(username=username, password=password)
          if user is not None:
              auth_login(request, user)
              print("login success")  
              return redirect("blog:dashboard")  # Redirect to a success page.
              
       
    return render(request, 'blog/login.html', {'form': form})

def dashboard(request):
    blog_title = "My Posts"
    #getting user posts
    all_posts = Post.objects.filter(user=request.user)
    
    #paginate
    paginator = Paginator(all_posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/dashboard.html', {"blog_title": blog_title, 'page_obj': page_obj})

def logout(request):
    auth_logout(request)
    return redirect("blog:index")

def forgot_password(request):
    form = ForgotPasswordForm()
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()

            if not user:
                messages.error(request, "No account found with this email.")
                return redirect("blog:forgot_password")

            # Generate token and UID
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Get domain
            current_site = get_current_site(request).domain

            # Build Reset Link URL
            reset_link = f"http://{current_site}/reset_password/{uid}/{token}/"

            subject = "Password Reset Requested"
            message = f"Click the link below to reset your password:\n\n{reset_link}"

            # ✅ FIXED: Added recipient_list as a LIST
            send_mail(subject, message, 'noreply@example.com', [email])

            messages.success(request, "Password reset email has been sent.")
            return redirect("blog:forgot_password")

    return render(request, 'blog/forgot_password.html', {'form': form})


def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password']
                user.set_password(new_password)
                user.save()
                messages.success(request, "Your password has been reset successfully.")
                return redirect("blog:login")
        else:
            form = ResetPasswordForm()

        return render(request, 'blog/reset_password.html', {'form': form})
    else:
        messages.error(request, "The reset link is invalid or expired. Please request a new password reset.")
        return redirect("blog:forgot_password")

def new_post(request):
        categories = Category.objects.all()
        form = PostForm()
        if request.method == 'POST':
            #form
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                return redirect('blog:dashboard')
        return render(request, 'blog/new_post.html', {'categories': categories, 'form': form})

def edit_post(request, post_id):
    categories = Category.objects.all()
    post = get_object_or_404(Post, id=post_id)
    form = PostForm()

    if request.method == "POST":
        #form
        form =PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully.")
            return redirect('blog:dashboard')
        
    return render(request, 'blog/edit_post.html', {'categories': categories, 'post': post, 'form': form})

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    messages.success(request, "Post deleted successfully.")
    return redirect('blog:dashboard')
    
    return render(request, 'blog/delete_post.html', {'post': post})