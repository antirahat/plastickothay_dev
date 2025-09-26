from django.shortcuts import render, redirect
from django.contrib import messages
from fileupload import upload_to_drive
from plastickothay.models import Post
from superadmin.models import User
from bson import ObjectId
from datetime import datetime, timedelta
import uuid, json
from email_control import post_mail, test_email

def get_user(user_id):
    try:
        return User.objects.get(pk=ObjectId(user_id))
    except User.DoesNotExist:
        return None
    except Exception as e:
        return None

def home (request):
    if 'user_id' not in request.session:
        if request.COOKIES.get('remember_me') == '1' and request.COOKIES.get('user_id'):
            request.session['user_id'] = request.COOKIES.get('user_id')

    user = None
    if 'user_id' in request.session:
        try:
            user_id = request.session.get('user_id')
            user = get_user(user_id)
        except:
            user = None       

    if request.method == "POST" :
        name = request.POST.get("nameData")
        phone = request.POST.get("phoneData")
        email = request.POST.get("emailData")
        severity = request.POST.get("severityData")
        photo_data = request.POST.get("photoData")
        lat = request.POST.get("latData")
        lon = request.POST.get("lonData")
        description = request.POST.get("descriptionData") or "No Description"
                
        if photo_data and ';base64,' in photo_data:
            header, base64_data = photo_data.split(';base64,')
            file_ext = header.split('/')[-1]
            filename = f"{uuid.uuid4()}.{file_ext}"
            response = upload_to_drive(photo_data, filename)

        if response :
            post = Post(
                user = user,
                name=name,
                email=email,
                pN=phone,
                severity=severity,
                imageID=response["id"],
                lat=lat,
                lon=lon,
                description=description
            )
            post.save()
            messages.success(request, "Report submitted successfully.")
            return redirect("plastickothay:home")
        else :
            messages.error(request, "Something went wrong.")
            return redirect("plastickothay:home")    

    posts = json.loads(Post.objects(status=1).to_json())
    
    context = {
        "posts" : posts,
        "user" : user,
    }
    print("Test Mail")
    test_email()

    return render(request, "plastickothay/index.html", context)

def posts(request):
    if 'user_id' in request.session:
        try:
            user_id = request.session.get('user_id')
            user = get_user(user_id)
        except:
            user = None
    else:
        user = None

    filter_type = request.GET.get('filter', 'all')  # default is 'all'
    now = datetime.now()

    if filter_type == 'today':
        start = datetime(now.year, now.month, now.day)
        posts = Post.objects(created__gte=start).order_by('-created')
    elif filter_type == 'last_week':
        start = now - timedelta(days=7)
        posts = Post.objects(created__gte=start).order_by('-created')
    elif filter_type == 'last_28_days':
        start = now - timedelta(days=28)
        posts = Post.objects(created__gte=start).order_by('-created')
    elif filter_type.startswith('severity_'):
        try:
            sev = int(filter_type.split('_')[1])
            posts = Post.objects(severity=sev).order_by('-created')
        except:
            posts = Post.objects().order_by('-created')
    elif filter_type == 'accepted':
        posts = Post.objects(status=1).order_by('-created')
    elif filter_type == 'pending':
        posts = Post.objects(status=2).order_by('-created')
    else:
        posts = Post.objects().order_by('-created')

    index = request.GET.get("index")

    context = {
        "posts": posts.order_by('-created')[:10],  # First 10 posts for "load more"
        "user": user,
    }
    return render(request, "plastickothay/posts.html", context)

def post(request, id) :
    if 'user_id' in request.session:
        try:
            user_id = request.session.get('user_id')
            user = get_user(user_id)
        except:
            user = None
    else:
        user = None

    post = Post.objects(id=ObjectId(id)).first()

    if request.method == "POST" :
        description = request.POST.get("description")
        post.description = description
        post.save()
        return redirect("plastickothay:post", id = post.id)

    context = {
        "post" : post,
        "user" : user,
    }

    return render(request, "plastickothay/post.html", context)

def contact(request) :
    return render(request, "plastickothay/contact.html")

def feedback(request) :
    if 'user_id' in request.session:
        try:
            user_id = request.session.get('user_id')
            user = get_user(user_id)
        except:
            user = None
    else:
        user = None
    # print(user)
    context = {
        "user" : user,
    }
    return render(request, "plastickothay/rateus.html", context)