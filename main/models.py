from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  


class Subject(models.Model):

    name = models.CharField(max_length=255, verbose_name='Fanlar')
    slug = models.SlugField(unique=True)
    logo = models.ImageField(verbose_name='Logo', null=True, blank=True)
    
    def __str__(self):
        return self.name


class Question(models.Model):

    subject = models.ForeignKey(Subject, verbose_name='Fan nomi', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Savol matni')
    asked_date = models.DateTimeField(auto_now=True, verbose_name='Savol berilgan vaqt')
    point = models.IntegerField()
    
    class Meta:
        ordering = ['asked_date']

    def __str__(self):
        return self.text

    
class QuestionImage(models.Model):
    question = models.ForeignKey(Question, default=None, on_delete=models.CASCADE, related_name='images')
    images = models.FileField()

    def __str__(self):
        return self.question.text


class Answer(models.Model):
    question = models.ForeignKey(Question, verbose_name='Savol',  related_name='answers', on_delete=models.CASCADE)
    user = models.ForeignKey(User,  related_name='answers', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Javob matni', null=True)
    answered_date = models.DateTimeField(auto_now=True, verbose_name='Javob berilgan vaqt')
    subject = models.ForeignKey(Subject, verbose_name='Savol', related_name='answers', on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Rasm', null=True, blank=True)
    is_best = models.BooleanField(default=False)

    def __str__(self):
        return '{} savolning javobi: '.format(self.question.text)

    
class AnswerImage(models.Model):
    answer = models.ForeignKey(Answer, default=None, on_delete=models.CASCADE, related_name='images')
    images = models.FileField()

    def __str__(self):
        return self.answer.text


class Comment(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


class Thank(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='thanks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='thanks')
    count = models.IntegerField(default=0) 

    def __str__(self):
        return self.answer


class Help(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='helps')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='helps')
    text = models.TextField()
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    rating = models.IntegerField(default=50)
    user_image = models.ImageField(verbose_name='User rasmi', default='default.png')
    status = models.CharField(verbose_name='Daraja', default='новычок', max_length=50)
    thanks = models.IntegerField(default=0)
    best_answers = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class RaitingCalc(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ball = models.IntegerField()
    ball_type = models.CharField(max_length=50)
    check_sum = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )