from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from bson import ObjectId
from datetime import datetime, timedelta
from superadmin.forms import LoginForm, CustomUserCreationForm
from superadmin.models import User
from plastickothay.models import Post
import json
from fileupload import delete_from_drive
from email_control import post_mail


def get_user(user_id: str) -> User | None:
    try:
        return User.objects.get(pk=ObjectId(user_id))
    except User.DoesNotExist:
        return None
    except Exception as e:
        return None
    
def wishes() -> str :
    now = datetime.now()
    hr = now.hour
    wish = "Evening"
    if (5 <= hr <= 12):
        wish = "Morning"
    if (13 <= hr <= 18):
        wish = "Afternoon"
    if (19 <= hr <= 24):
        wish = "Evening"
    return wish

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember = form.cleaned_data.get('remember_me')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                request.session['user_id'] = str(user.id)
                if not remember:
                    request.session.set_expiry(0)
                    response = redirect('superadmin:dashboard')
                    response.delete_cookie('remember_me')
                    response.delete_cookie('user_id')
                else:
                    request.session.set_expiry(1209600)
                    response = redirect('superadmin:dashboard')
                    response.delete_cookie('remember_me')
                    response.delete_cookie('user_id')
                    response.set_cookie('remember_me', '1', max_age=1209600, httponly=True, samesite='Lax')
                    response.set_cookie('user_id', str(user.id), max_age=1209600, httponly=True, samesite='Lax')

                return response
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

        # If remember_me cookie is set, redirect automatically
        if request.COOKIES.get('remember_me') == '1' and request.COOKIES.get('user_id'):
            request.session['user_id'] = request.COOKIES.get('user_id')
            return redirect('superadmin:dashboard')

    return render(request, 'superadmin/login.html', {'form': form})

def register(request) :
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. Please log in.")
            return redirect('superadmin:login')  # Update with your login URL name
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'superadmin/createaccount.html', {'form': form})

def dashboard(request) :
    if request.session.get('user_id'):
        user_id = request.session.get('user_id')
        user = get_user(user_id)

        wish = wishes()

        recent_posts = list()
        pending_posts = list()
        accept_posts = list()        
        days = list()
        for i in range(28):
            day_start = datetime.now().date() - timedelta(days=i)
            day_end = day_start + timedelta(days=1)
            start_datetime = datetime.combine(day_start, datetime.min.time())
            end_datetime = datetime.combine(day_end, datetime.min.time())
            post_cnt = Post.objects(created__gte=start_datetime, created__lt=end_datetime).count()
            accept_cnt = Post.objects(created__gte=start_datetime, created__lt=end_datetime, status = 1).count()
            pending_cnt = Post.objects(created__gte=start_datetime, created__lt=end_datetime, status = 2).count()
            recent_posts.append(post_cnt)
            accept_posts.append(accept_cnt)
            pending_posts.append(pending_cnt)
            days.append(day_start.strftime("%b %d"))

        days.reverse()
        recent_posts.reverse()
        pending_posts.reverse()

        days = json.dumps(days)
        
        negative_pending_posts = list(ele * (-1) for ele in pending_posts)

        day_start = datetime.now().date() - timedelta(days=i)        
        start_datetime = datetime.combine(day_start, datetime.min.time())
        accept_count = Post.objects(created__gte=start_datetime, status = 1).count()
        reject_count = Post.objects(created__gte=start_datetime, status = 0).count()
        pending_count = Post.objects(created__gte=start_datetime, status = 2).count()

        context = {
            "user" : user, 
            "wish" : wish,
            "recent_post" : recent_posts,
            "pending_post": pending_posts,
            "accept_post" : accept_posts,
            "negative_pending_post" : negative_pending_posts,
            "days" : days,
            "accept_count" : accept_count,
            "reject_count" : reject_count,
            "pending_count" : pending_count,
        }

        return render(request, 'superadmin/dashboard.html', context)
    else :
        return redirect('superadmin:login')
    
def accept_post(request, id: str) :
    next_url = request.GET.get("next", "/")

    post = Post.objects(id=ObjectId(id)).first()
    try :
        flage = post_mail(post)
        if flage :
            post.status = 1
            post.save()        
            messages.success(request, "Post has been accepted.")
        else :
            messages.error(request, "Unable to send email to the post creator.")
    except Exception as e :
        messages.error(request, f"An error occurred: {str(e)}.")

    return redirect(next_url)

def reject_post(request, id: str) :
    next_url = request.GET.get("next", "/")

    post = Post.objects(id=ObjectId(id)).first()
    try :
        is_deleted = delete_from_drive(post.imageID)
        if is_deleted :
            post.delete()
            messages.success(request, "Post has been deleted.")
        else :
            messages.success(request, "File not found.")
    except Exception as e :
        messages.error(request, f"An error occurred: {str(e)}.")

    return redirect(next_url)


def logout_view(request) :
    if request.session.get('user_id'):
        user_id = request.session.get('user_id')
        user = get_user(user_id)
        if user :
            user.is_active = False
            user.save()
            del request.session["user_id"]
            request.session.set_expiry(0)
            response = redirect('superadmin:login')
            response.delete_cookie('remember_me')
            response.delete_cookie('user_id')
            return response
    else :
        return redirect("superadmin:dashboard")