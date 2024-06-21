from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField

class BloggerManager(models.Manager):
    def user(self, uname):
        return super().get_queryset().filter(username=uname).exists()
    def email(self, email):
        return super().get_queryset().filter(email=email).exists()
    def phone(self, phone):
        return super().get_queryset().filter(phone=phone).exists()
    def get_by_natural_key(self, username):
        return self.get(username=username)

            
class BloggerSignup(AbstractUser):
    phone = models.CharField(max_length=11, unique=True, default="")
    email = models.EmailField(max_length=255, unique=True)
    middle_name = models.CharField(max_length=100, null=True, default="")
    gender = models.CharField(max_length=6, default="")
    address = models.CharField(max_length=256, default="")
    dob = models.DateField(default="")

    blogger = BloggerManager()

    class Meta:
        db_table = "BloggerSignup"

    def __str__(self):
        return self.username

# class Content_Manager(models.Manager):
#     def total_content(self):
#         return super().get_queryset().count()
#     def category_content_count(self, search):
#         query = f"SELECT CONCAT(COUNT(*), 'post') AS Post FROM Content WHERE category='{search}' GROUP BY category ORDER BY category"
#         return super().get_queryset().raw(query)
#     def category_content(self, search):
        # return super().get(category=search)
    
class BloggerContent(models.Model):
    # blogger = models.ForeignKey(BloggerSignup, on_delete=models.CASCADE, to_field='username')
    # headline = models.CharField(max_length=255, null=False, default='')
    content = RichTextField(default='')
    # creation_date = models.DateTimeField(default=timezone.now, editable=False,)
    # update = models.DateTimeField(auto_now=True,)
    # category = models.CharField(max_length=20, null=False, default='')

    class Meta:
        db_table = 'BloggerContent'
    
    def __str__(self):
        return self.headline

class ProfilePicture(models.Model):
    profile_picture = models.OneToOneField(BloggerSignup, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pictures/', default='R.jpg', null=True, blank=True, height_field='100', width_field='100')

    class Meta:
        db_table = 'profile_picture'