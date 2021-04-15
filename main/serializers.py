from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = ('user_id', 'rating', 'user_image', 'status', 'thanks', 'best_answers')
        

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined', 'password', 'profile', )

    def validate(self, attrs):
        username = attrs.get('username',)
        email = attrs.get('email')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({
                'error': "Username is not available"})
        elif User.objects.filter(email=email).exists():
            raise serializers.ValidationError({
                'error': 'Email is already registered',
                })
        
        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=make_password(validated_data['password'])
        )
        

class QuestionImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionImage
        fields = ('images', )


class AnswerImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnswerImage
        fields = ('images',)


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('user_id', 'answer_id', 'text', 'created_date',)


class HelpSerializer(serializers.ModelSerializer):

    class Meta:
        model = Help
        fields = ('user_id', 'question',  'text', 'created_date',)


class RatingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RaitingCalc
        fields = '__all__'


class ThanksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Thank
        fields = ('user_id', )


class AnswerSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, required=False)
    user = UserSerializer(many=False, required=False)
    subject = SubjectSerializer(many=False, required=False)
    thanks = ThanksSerializer(many=True, required=False)
    images = AnswerImagesSerializer(many=True, required=False)

    class Meta:
        model = Answer
        fields = ('id', 'question_id', 'user_id', 'text', 'answered_date', 'images', 'is_best',
                  'subject', 'thanks', 'comments', 'user')


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    helps = HelpSerializer(many=True, required=False)
    answers = AnswerSerializer(many=True, required=False)
    subject = SubjectSerializer(many=False, required=False)
    user = UserSerializer(many=False, required=False)
    images = QuestionImagesSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ('id', 'text', 'asked_date', 'point', 'subject_id', 'helps', 'answers',  'subject', 'images', 'user')


class UserDetailSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)
    questions = QuestionSerializer(many=True)
    answers = AnswerSerializer(many=True)

    class Meta:
        model = User
        fields = ('username', 'date_joined', 'profile', 'questions', 'answers')


class SubjectsSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Subject
        fields = ('id', 'name', 'slug', 'questions')


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
