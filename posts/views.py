from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views import View
from .models import Posts, Comments
from django.utils.decorators import method_decorator
from users.utils import decode_jwt,custom_login_required
from users.views import Users

# Create your views here.
class CreatePost(View):

    @method_decorator(custom_login_required)
    def get(self, request):
        return render(request, 'create_post.html')
    
    @method_decorator(custom_login_required)
    def post(self, request):

        token = request.COOKIES.get('auth_token')
        payload = decode_jwt(token)
        user_id = payload.get('id')
        try:
            title = request.POST['title']
            content = request.POST['content']
            image = request.FILES.get('image', None)
            
             # Create the post object
            post = Posts(
                title=title,
                content=content,
                user_id=user_id
            )
            if image:
                post.image = image
            
            post.save()
            return redirect('home')
        except Exception as e:
            print(e)
            return redirect('create_post')
        
class CreateComment(View):

    @method_decorator(custom_login_required)
    def get(self, request, post_id):
        token = request.COOKIES.get('auth_token')
        
        payload = decode_jwt(token)
        user_id = payload.get('id')

        post = get_object_or_404(Posts, id=post_id)
        user = get_object_or_404(Users, id=user_id)
        comments = Comments.objects.filter(post_id=post_id, reply_to__isnull=True)
        
        return render(request, 'create_comment.html', {'post':post, 'comments':comments, 'user':user})


    @method_decorator(custom_login_required)
    def post(self, request, post_id):
        token = request.COOKIES.get('auth_token')
        payload = decode_jwt(token)
        user_id = payload.get('id')

        post = get_object_or_404(Posts, id=post_id)
        user = get_object_or_404(Users, id=user_id)

        comment_text = request.POST.get('comment_text')
        comment = Comments(post=post, name=user, comment_text=comment_text)
        comment.save()
        return redirect('home')
    

class CommentReply(View):

    @method_decorator(custom_login_required)
    def get(self, request, comment_id):
        token = request.COOKIES.get('auth_token')
        payload = decode_jwt(token)
        user_id = payload.get('id')
        user = get_object_or_404(Users, id=user_id)
        comment = Comments.objects.get(id=comment_id)
        replies = Comments.objects.filter(reply_to=comment.id)
        return render(request, 'comment_reply.html', {"user":user, "comment": comment, "replies":replies})
    

    @method_decorator(custom_login_required)
    def post(self, request, comment_id):
        token = request.COOKIES.get('auth_token')
        payload = decode_jwt(token)
        user_id = payload.get('id')

        comment = Comments.objects.get(id=comment_id)
        user = Users.objects.get(id=user_id)
        post = comment.post
        post_id = post.id
        comment_text = request.POST['reply']

        reply = Comments(post=post, name=user, comment_text=comment_text, reply_to=comment)
        reply.save()
        return redirect('create_comment', post_id)




@method_decorator(custom_login_required)
def delete_post(request, post_id):
    post = Posts.objects.get(id=post_id)
    post.delete()
    return redirect('home')

@method_decorator(custom_login_required)
def like_post(request, post_id):
    token = request.COOKIES.get('auth_token')
    payload = decode_jwt(token)
    user_id = payload.get('id')

    post = get_object_or_404(Posts, id=post_id)
    user = get_object_or_404(Users, id=user_id)

    if post.likes.filter(id=user_id).exists():
        post.likes.remove(user)
        return redirect('home')
    else:
        post.likes.add(user)
        return redirect('home')

@method_decorator(custom_login_required)
def save_post(request, post_id):
    token = request.COOKIES.get('auth_token')
    payload = decode_jwt(token)
    user_id = payload.get('id')

    post = get_object_or_404(Posts, id=post_id)
    user = get_object_or_404(Users, id=user_id)

    if post.saves.filter(id=user_id).exists():
        post.saves.remove(user)
        return redirect('home')
    else:
        post.saves.add(user)
        return redirect('home')
    
@method_decorator(custom_login_required)
def delete_comment(request, comment_id):
    comment = Comments.objects.get(id=comment_id)
    post_id = comment.post.id

    comment.delete()
    return redirect('create_comment', post_id)

custom_login_required
def comment_like(request, comment_id):
    token = request.COOKIES.get('auth_token')
    payload = decode_jwt(token)
    user_id = payload.get('id')
    user = Users.objects.get(id=user_id)
    comment = Comments.objects.get(id=comment_id)
    post_id = comment.post.id

    if comment.likes.filter(id=user_id).exists():
        comment.likes.remove(user)
        return redirect('create_comment', post_id)
    else:
        comment.likes.add(user)
        return redirect('create_comment', post_id)