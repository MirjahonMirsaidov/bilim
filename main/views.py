from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, hashers
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from django.contrib import auth
from django.db.models import Count
from django.http import JsonResponse
from rest_framework import viewsets, generics, status, filters, pagination, mixins
from rest_framework.decorators import api_view
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser
from .models import *
from .serializers import *
import hashlib


@api_view(['GET', ])
def apiOverview(request):
    api_urls = {
        'Subjects': '/subjects/',
        'Questions': '/questions/',
        'Question-Detail': '/question-detail/<str:pk>/',
        'Create': '/question-create/',
        'Update': '/question-update/<str:pk>/',
        'Delete': '/question-delete/<str:pk>/',
        'Users': '/users/',
        'User-detail': 'user-detail/<str:pk>/',
    }

    return Response(api_urls)


class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    pagination_class = None

class RegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            username = request.data.get('username')
            id = User.objects.get(username=username).id
            profile = Profile.objects.get_or_create(user_id=id)
            point = request.user.profile.rating

            return Response("Registration success", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsernameCheckView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        username = request.data.get('username')

        checked = User.objects.filter(username=username).exists()

        if checked:
            return Response({
                'status': 400,
                'data': 'Имя пользователя не доступно',
            })
        else:
            return Response({
                'status': 200,
                'data': 'Доступно',
            })


class LoginView(APIView):
    permission_classes = []
    serializer_class = UserSerializer

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'token': token.key,
                'user_id': user.pk,
                'username': username
            })
        return Response({'response': 'user not found'})


class MeView(APIView):
    def get(self, request):
        user = request.user
        point = user.profile.rating
       
        
        if 0 < point < 100:
            user.profile.status = 'новичок'
            user.profile.save()
        elif 100 <= point < 300:
            user.profile.status = 'середнячок'
            user.profile.save()
        elif 300 <= point < 500:
            user.profile.status = 'хорошист'
            user.profile.save()
        elif 500 <= point < 1000:
            user.profile.status = 'умный'
            user.profile.save()
        elif 1000 <= point < 3000:
            user.profile.status = 'отличник'
            user.profile.save()
        elif 3000 <= point < 5000:
            user.profile.status = 'ученый'
            user.profile.save()
        elif 5000 <= point < 8000:
            user.profile.status = 'почетный грамотей'
            user.profile.save()
        else:
            user.profile.status = 'профессор'
            user.profile.save()

        return Response({
            'status': 200,
            'data': {
                'user': {
                    'user_id': user.pk,
                    'username': user.username,
                    'date_joined': user.date_joined,
                    'rating': user.profile.rating,
                    'status': user.profile.status,
                    'image': 'http://192.168.1.8:8000'+user.profile.user_image.url,
                }
            }
        })


class LogoutView(APIView):

    def delete(self, request, format=None):
        request.user.auth_token.delete()
        return Response("Logout Success")


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()

    # def get(self, request, pk):
    #     serializer = QuestionSerializer(data=request.data)
    #     user = User.objects.get(pk=pk)
    #     questions_count = Question.objects.filter(user_id=user.pk).count()
    #     answers_count = Answer.objects.filter(user_id=user.pk).count()
    #     questions = Question.objects.filter(user=pk).values()
    #     answers = Answer.objects.filter(user_id=pk).values()

    #     return Response({
    #             'status': 200,
    #             'data': {
    #                 'id': user.pk,
    #                 'username': user.username,
    #                 'image': 'http://192.168.1.8:8000'+user.profile.user_image.url,
    #                 'questions_count': questions_count,
    #                 'answers_count': answers_count,
    #                 'thanks': user.profile.thanks,
    #                 'best_answers': user.profile.best_answers,
    #                 },

    #             'questions':  questions,
    #             'answers' : answers,

    #             })


class UserUpdateView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def patch(self, request):
        serializer = UserSerializer(data=request.data)
        user = request.user
        username = request.data.get('username')
        user_image = request.data.get('user_image')
        if user_image:
            if username == user.username or username is None or username == '':
                user.profile.user_image = user_image
                user.profile.save()
                return Response("Image successfuly updated")
            else:
                user.profile.user_image = user_image
                user.username = username
                user.save()
                user.profile.save()
                return Response("Username and image successfuly updated")
        elif username != user.username and username.exists():
            user.username = username
            user.save()
            return Response({
                'status': 200,
                'data': {
                    'username': username,

                },
            })
        else:
            return Response("O'zgarish amalga oshiring!")


# class UserDeleteView(generics.DestroyAPIView):
#     permission_classes = [IsAuthenticated, ]
#     serializer_class = UserSerializer
#     lookup_field =
#     queryset = User.objects.all()

#     def get_object(self):
#         try:
#             instance = self.queryset.get(username=self.request.user.username)
#             return instance
#         except User.DoesNotExist:
#             raise Http404


class UserDeleteView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        self.object = self.request.user
        user = request.user
        password = request.data.get('password')

        if not self.object.check_password(password):
            return Response({
                'error': "Wrong password."
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.delete()
            return Response({
                'succes': 'User deleted successfully!'}, status=status.HTTP_200_OK
            )

    def get_object(self):
        try:
            instance = self.queryset.get(username=self.request.user.username)
            return instance
        except User.DoesNotExist:
            raise Http404


class UserQuestionsView(generics.ListAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        questions = Answer.objects.filter(user=self.kwargs['user_id'])

        return questions


class UserAnswersView(generics.ListAPIView):
    serializer_class = AnswerSerializer

    def get_queryset(self):
        answers = Answer.objects.filter(user=self.kwargs['user_id'])

        return answers


class SubjectQuestionView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    
    def get_queryset(self):

        subject_questions = Question.objects.all()
        slug = self.kwargs['slug']
        subject_id = Subject.objects.get(slug=slug).id

        if subject_id is not None:
            subject_questions = Question.objects.filter(subject=subject_id)

        return subject_questions


class QuestionListView(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer
    # Searching parametrs /Qidiruv bo'yicha sozlamalar
    search_fields = ['text']
    filter_backends = (filters.SearchFilter,)

    def get_queryset(self):

        queryset = Question.objects.order_by('-id')
        return queryset


class QuestionDetailView(generics.RetrieveAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


class QuestionUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = QuestionSerializer

    def post(self, request, pk):
        serializer = QuestionSerializer(data=request.data)
        question = Question.objects.get(id=pk)
        text = request.data.get('text')
        point = request.data.get('point')
        if serializer.is_valid():
            question.text = text
            question.point = point
            question.save()
            return Response({
                'status': 200,
                'data': {
                    'id': question.id,
                    'question_text': question.text,
                    'question_point': question.point,

                }
            })
        return Response(serializer.errors,)


class QuestionDeleteView(generics.DestroyAPIView):
    serializer_class = QuestionSerializer

    def delete(self, request, pk):
        question = Question.objects.get(id=pk)
        if question:
            question.delete()
            return Response({
                'status': 200,
                'data': 'Question is deleted',

            })







class AnswerListView(generics.ListAPIView):
    serializer_class = AnswerSerializer

    def get_queryset(self):

        queryset = Answer.objects.all()
        return queryset


class AnswerDetailView(generics.RetrieveAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class AnswerUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = AnswerSerializer

    def post(self, request, pk):
        serializer = AnswerSerializer(data=request.data)
        answer = Answer.objects.get(id=pk)
        text = request.data.get('text')
        if serializer.is_valid():
            answer.text = text
            answer.save()
            return Response({
                'status': 200,
                'data': {
                    'id': answer.id,
                    'answer_text': answer.text,
                }
            })


class AnswerDeleteView(generics.DestroyAPIView):
    serializer_class = AnswerSerializer

    def delete(self, request, pk):
        answer = Answer.objects.get(id=pk)
        if answer:
            answer.delete()
            return Response({
                'status': 200,
                'data': 'Answer is deleted',

            })


class RaitingListView(generics.ListAPIView):
    serializer_class = RatingSerializer

    def get_queryset(self):
        queryset = RaitingCalc.objects.all()
        return queryset



class UsersByRatingView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.order_by('-profile__rating')
        return queryset



class CommmentListView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.all()
        return queryset


class ChangePasswordView(generics.UpdateAPIView):
    """
    Change user password 
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = request.user
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': {
                    'username': user.username,
                }
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommmentCreateView(generics.GenericAPIView):
    serializer_class = CommentSerializer

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        answer_id = request.data.get('answer')
        text = request.data.get('text')
        user_id = request.user.pk
        if serializer.is_valid():
            serializer.save(user_id=user_id, answer_id=answer_id, text=text)
            return Response({
                'status': 200,
                'data': {
                    'user_id': user_id,
                    'answer_id': answer_id,
                    'commment': text,

                },
            })

        return Response(serializer.errors)


class BestCreateView(generics.GenericAPIView):
    serializer_class = AnswerSerializer

    def post(self, request):
        serializer = AnswerSerializer(data=request.data)
        answer_id = request.data.get('answer_id')
        answer = Answer.objects.get(id=answer_id)
        user_id = answer.user_id
        user = User.objects.get(id=user_id)
        best_answers = Profile.objects.get(user_id=user_id).best_answers
        is_best = request.data.get('is_best')
        if serializer.is_valid():
            if is_best:
                answer.is_best = is_best
                answer.save()
                best_answers += 1
                user.profile.best_answers = best_answers
                user.profile.save()
                return Response({
                    'status': 200,
                    'data': 'Best is True'
                })
            return Response('False')
        return Response(serializer.errors)



class HelpListView(generics.ListAPIView):
    serializer_class = HelpSerializer

    def get_queryset(self):
        queryset = Help.objects.all()
        return queryset



class HelpCreateView(generics.GenericAPIView):
    serializer_class = HelpSerializer

    def post(self, request):
        serializer = HelpSerializer(data=request.data)
        question_id = request.data.get('question')
        text = request.data.get('text')
        user_id = request.user.pk
        if serializer.is_valid():
            serializer.save(user_id=user_id,
                            question_id=question_id, text=text)
            return Response({
                'status': 200,
                'data': {
                    'user_id': user_id,
                    'question_id': question_id,
                    'commment': text,

                },
            })

        return Response(serializer.errors)



class QuestionCreateView(generics.CreateAPIView):
    serializer_class = QuestionSerializer

    def post(self, request):
        m = hashlib.md5()
        serializer = QuestionSerializer(data=request.data)
        subject = request.data.get('subject')
        text = request.data.get('text')
        length = request.data.get('length')
        user_id = request.user.pk
        ball = -int(request.data.get('point'))
        ball_type = 'savol'
        user = RaitingCalc.objects.filter(user=user_id).exists()

        if user:
            data_is = RaitingCalc.objects.filter(
                user_id=user_id).last().check_sum
            m = hashlib.md5(
                str(data_is+str(user_id)+str(ball)+ball_type).encode('utf-8'))
            check_sum = m.hexdigest()
            print(data_is)
            print(check_sum)

        else:
            m = hashlib.md5(
                str(str(user_id)+str(ball)+ball_type).encode('utf-8'))
            check_sum = m.hexdigest()
            print(check_sum)
        subjectcheck = Subject.objects.filter(id=subject).exists()
        print(subjectcheck)
        if subjectcheck is None or subjectcheck is False:
            return Response({
                'status': 400, 
            })
        if serializer.is_valid():
            user = Profile.objects.get(user=user_id)
            profile_ball = Profile.objects.get(user=user_id).rating
            if (-ball) <= profile_ball:

                profile_ball += int(ball)
                user.rating = profile_ball
                user.save()
                question = serializer.save(subject_id=subject, user_id=user_id)
                print(question)
                RaitingCalc.objects.create(
                    user_id=user_id, check_sum=check_sum, ball=ball, ball_type=ball_type)
                for file_num in range(0, int(length)):
                    images = request.FILES.get(f'images{file_num}')
                    QuestionImage.objects.create(
                        question=question,
                        images=images
                    )
                    print(images,request.data)

                return Response({
                    'status': 200,
                    'data': {
                        'username': request.user.username,
                        'subject': subject,
                        'question': text,
                        'point': -ball,
                    }
                },)
            else:
                return Response(f'Savol uchun bergan ballingiz {profile_ball} dan katta')

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AnswerCreateView(generics.CreateAPIView):
    serializer_class = AnswerSerializer

    def post(self, request):
        m = hashlib.md5()
        serializer = AnswerSerializer(data=request.data)
        question = request.data.get('question')
        text = request.data.get('text')
        length = request.data.get('length')
        user_id = request.user.pk
        ball = Question.objects.get(id=question).point
        subject = Question.objects.get(id=question).subject_id
        ball_type = 'javob'
        user = RaitingCalc.objects.filter(user=user_id).exists()

        if user:
            data_is = RaitingCalc.objects.filter(
                user_id=user_id).last().check_sum
            m = hashlib.md5(str(data_is + str(user_id) +
                                str(ball) + ball_type).encode('utf-8'))
            check_sum = m.hexdigest()
            print(data_is)
            print(check_sum)

        else:
            m = hashlib.md5(
                str(str(user_id) + str(ball) + ball_type).encode('utf-8'))
            check_sum = m.hexdigest()
            print(check_sum)

        if serializer.is_valid():
            user = Profile.objects.get(user=user_id)
            profile_ball = Profile.objects.get(user=user_id).rating
            print(profile_ball)
            profile_ball += int(ball)
            user.rating = profile_ball
            print(user.rating)
            user.save()

            answer = serializer.save(question_id=question,
                            user_id=user_id, subject_id=subject)
            RaitingCalc.objects.create(
                user_id=user_id, check_sum=check_sum, ball=ball, ball_type=ball_type)
            
            for file_num in range(0, int(length)):
                    images = request.data.get(f'images{file_num}')
                    AnswerImage.objects.create(
                        answer=answer,
                        images=images
                    )
                    print(images,request.data)

            return Response({

                'status': 200,
                'data': {
                    'user': user.pk,
                    'question_id': question,
                    'answer': text,

                }
            },
                status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ThanksView(generics.CreateAPIView):
    serializer_class = AnswerSerializer

    def post(self, request):
        serializer = AnswerSerializer(data=request.data)
        answer_id = request.data.get('id')
        thanks = 1
        answer = Answer.objects.get(id=answer_id)
        user_id = request.user.pk
        answerid = Thank.objects.filter(user_id=user_id, answer_id=answer_id)
        if answerid:
            return Response("Faqat bir marta")
        else:
            thank = Thank.objects.create(
                answer_id=answer_id, count=thanks, user_id=user_id)
        thank.save()
        user = User.objects.get(id=answer.user_id)
        user.profile.thanks += 1
        user.profile.save()

        return Response({
            'status': 200,
            'data': {
                'answer': answer.text,
            },
        })



class BaseView(View):

    def get(self, request):

        subjects = Subject.objects.all()
        questions = Question.objects.order_by("-id")[:6]

        context = {
            'subjects': subjects,
            'questions': questions
        }
        return render(request, 'base.html', context)
