from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, username, stu_email, password, **extra_fields):
        if not stu_email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(stu_email)
        user = self.model(username=username, stu_email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, stu_email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, stu_email, password, **extra_fields)


class Users(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="pfp/", default="pfp/blank_profile.png", null=True, blank=True)
    stu_email = models.CharField(max_length=45, unique=True)
    password = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['stu_email', 'password']

    class Meta:
        db_table = 'users'

class CalendarEvent(models.Model):
    event_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=30)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    color = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('Users', models.CASCADE)

    class Meta:
        db_table = 'calendar_event'

class CompanionFAQCategory(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'companion_faq_category'

    def __str__(self):
        return self.name

class CompanionFAQ(models.Model):
    category = models.ForeignKey(CompanionFAQCategory, models.CASCADE)
    question = models.TextField(null=False, blank=False)
    answer = models.TextField(null=False, blank=False)
    keywords = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def getFirstKeyword(self):
        return self.keywords.split(', ')[0]

    def getOtherKeywords(self):
        return self.keywords.split(', ')[1:]

    def hasMultipleKeywords(self):
        return self.keywords.count(',') > 0

    class Meta:
        db_table = 'companion_faq'

class Flair(models.Model):
    flair_id = models.AutoField(primary_key=True)
    flair_color = models.CharField(max_length=30)
    flair_name = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'flair'

    def __str__(self):
        return self.flair_name


class Posts(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    flair = models.ForeignKey('Flair', models.CASCADE)
    user = models.ForeignKey('Users', models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def getUpvotes(self):
        return PostVotes.objects.filter(post_id=self.post_id, post_upvote=True).count()

    def getDownvotes(self):
        return PostVotes.objects.filter(post_id=self.post_id, post_upvote=False).count()

    # def isUpVoted(self):
    #     return PostVotes.objects.filter(post_id=self.post_id, user_id=self.user.user_id, post_upvote=True).exists()
    #
    # def isDownVoted(self):
    #     return PostVotes.objects.filter(post_id=self.post_id, user_id=self.user.user_id, post_upvote=False).exists()

    def getComments(self):
        return PostComments.objects.filter(post_id=self.post_id).count()

    # def getSaves(self):
    #     return Saves.objects.filter(post_id=self.post_id).count()

    class Meta:
        db_table = 'posts'


class PostVotes(models.Model):
    post_vote_id = models.AutoField(primary_key=True)
    post_upvote = models.BooleanField(default=False)
    post = models.ForeignKey('Posts', models.CASCADE)
    user = models.ForeignKey('Users', models.CASCADE)

    class Meta:
        db_table = 'post_votes'


class PostComments(models.Model):
    post_comment_id = models.AutoField(primary_key=True)
    content = models.TextField()
    post = models.ForeignKey('Posts', models.CASCADE)
    user = models.ForeignKey('Users', models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def getUpvotes(self):
        return PostcVotes.objects.filter(post_comment_id=self.post_comment_id, postc_upvote=True).count()

    def getDownvotes(self):
        return PostcVotes.objects.filter(post_comment_id=self.post_comment_id, postc_upvote=False).count()

    class Meta:
        db_table = 'post_comments'


class PostcVotes(models.Model):
    postc_vote_id = models.AutoField(primary_key=True)
    postc_upvote = models.BooleanField(default=False)
    post_comment = models.ForeignKey(PostComments, models.CASCADE)
    user = models.ForeignKey('Users', models.CASCADE)

    class Meta:
        db_table = 'postc_votes'


class Saves(models.Model):
    pk = models.CompositePrimaryKey('saved_at', 'post_id', 'user_id')
    saved_at = models.DateTimeField()
    post = models.ForeignKey(Posts, models.CASCADE)
    user = models.ForeignKey('Users', models.CASCADE)

    class Meta:
        db_table = 'saves'


class UserComments(models.Model):
    user_comment_id  = models.AutoField(primary_key=True)
    profile_feedback = models.TextField(blank=False, null=False)
    profile_upvote   = models.BooleanField(default=False)
    profile_user_email = models.CharField(max_length=40)
    commenter = models.ForeignKey('Users', models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_comments'


class ReportPost(models.Model):
    user = models.ForeignKey('Users', models.CASCADE)
    post = models.ForeignKey('Posts', models.CASCADE)
    content = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'report_post'


class ReportComment(models.Model):
    user = models.ForeignKey('Users', models.CASCADE)
    comment = models.ForeignKey('PostComments', models.CASCADE)
    content = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'report_comment'


class ReportUser(models.Model):
    user = models.ForeignKey('Users', models.CASCADE, related_name='reporter')
    target = models.ForeignKey('Users', models.CASCADE, related_name='target_user')
    content = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'report_user'


class Notification(models.Model):
    user = models.ForeignKey('Users', models.CASCADE, related_name='giver')
    target = models.ForeignKey('Users', models.CASCADE, related_name='receiver')
    is_seen = models.BooleanField(default=False)
    vote = models.BooleanField(null=True)
    type = models.CharField(max_length=40)  # post_like/post_dislike/comment_like/comment_dislike/comment_add/profile_like/profile_dislike
    title = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notification'

# {user} like your {post_title}
# {user} dislike your {post_title}
# {user} like your comment in {post_title}
# {user} dislike your comment in {post_title}
# {user} commented on your {post_title}
# {user} gave an insightful on your profile
# {user} gave a thumbsdown on your profile

class Appeals(models.Model):
    user = models.ForeignKey('Users', models.CASCADE)
    reason = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'appeals'
