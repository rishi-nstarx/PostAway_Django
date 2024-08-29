from django.db import models
from django.utils import timezone
from users.models import Users
from ckeditor.fields import RichTextField

# https://djangocentral.com/understanding-related-name-in-django-models/#:~:text=In%20Django%2C%20related_name%20is%20an,reverse%20side%20of%20the%20relation.
# if you want to read about 'related_name=' attribute, follow the above given link.

class Posts(models.Model):

    class Meta:
        db_table = "posts"

    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = RichTextField(blank=True, null=True)
    image = models.ImageField(upload_to='photos/', blank=True, null=True)
    likes = models.ManyToManyField(Users, related_name="likedpost", blank=True)
    # comments = models.ManyToManyField(Users, related_name="post_comments", blank=True)
    saves = models.ManyToManyField(Users, related_name="savedpost", blank=True)
    time_created = models.DateTimeField(default=timezone.now)
    time_updated = models.DateTimeField(auto_now=True)

    def total_likes(self):
        return self.likes.count()

    # def total_comments(self):
    #     return self.comments.count()
    def total_comments(self):
        return self.comments.filter(reply_to__isnull=True).count()

    
    def total_save(self):
        return self.saves.count()
    
    def __str__(self):
        if len(self.title)>10:
            return f'{self.title[:10]}...'
        else:
            return self.title
    
 
class Comments(models.Model):

    class Meta:
        db_table = "comments"

    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comments')
    name = models.ForeignKey(Users, on_delete=models.CASCADE)
    comment_text = RichTextField(max_length=300)
    likes = models.ManyToManyField(Users, related_name='comment_likes', blank=True)
    reply_to = models.ForeignKey('self', on_delete=models.CASCADE, related_name='reply_on_comments', null=True)
    time_created = models.DateTimeField(default=timezone.now)
    time_updated = models.DateTimeField(auto_now=True)

    def total_comment_likes(self):
        return self.likes.count()
    
    def total_comment_replies(self):
        return self.reply.count()
    
    def __str__(self):
        return '%s - %s - %s' %(self.post.title, self.name, self.id)
