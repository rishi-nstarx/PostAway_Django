from django.shortcuts import render, HttpResponse, redirect
from users.utils import decode_jwt, custom_login_required
from users.models import Users
from posts.models import Posts

# Create your views here.

@custom_login_required
def home(request):
    token = request.COOKIES.get('auth_token')
    payload = decode_jwt(token)
    user_id = payload.get('id')
    user = Users.objects.get(id=user_id)
    posts = Posts.objects.all()
    return render(request, 'home.html', {'user':user, 'posts':posts})

@custom_login_required
def profile(request):
    return HttpResponse("Hey EveryOneon Profile...!")