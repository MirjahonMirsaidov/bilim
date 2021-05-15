from django.urls import path
from main.views import *


app_name = 'main'

urlpatterns = [
    path('subjects/', SubjectListView.as_view(), name="subjects"),
    path('subjects/<slug:slug>', SubjectQuestionView.as_view()),

    path('questions/', QuestionListView.as_view(), name="questions"),
    path('question-detail/<str:pk>/', QuestionDetailView.as_view(), name="question-detail"),
    path('question-create/', QuestionCreateView.as_view(), name="question-create"),
    path('question-update/<str:pk>/', QuestionUpdateView.as_view(), name="question-update"),
    path('question-delete/<str:pk>/', QuestionDeleteView.as_view(), name="question-delete"),

    path('answers/', AnswerListView.as_view(), name="answers"),
    path('answer-detail/<str:pk>/', AnswerDetailView.as_view(), name="answer-detail"),
    path('answer-create/', AnswerCreateView.as_view(), name="answer-create"),
    path('answer-update/<str:pk>/', AnswerUpdateView.as_view(), name="answer-update"),
    path('answer-delete/<str:pk>/', AnswerDeleteView.as_view(), name="answer-delete"),

    path('users/', UserListView.as_view(), name='users'),
    path('user-detail/<str:pk>/', UserDetailView.as_view(), name ='user-detail'),
    path('user-update/', UserUpdateView.as_view(), name='user-update'),
    path('change-password/', ChangePasswordView.as_view()),
    path('user-questions/<int:user_id>/', UserQuestionsView.as_view(), name='user-questions'),
    path('user-answers/<int:user_id>/', UserAnswersView.as_view(), name='user-answers'),
    path('user-delete/', UserDeleteView.as_view(), name='user-delete'),
    path('username-check/', UsernameCheckView.as_view(), name='username-check'),


    path('comment-create/', CommmentCreateView.as_view(), name='comment-create'),
    path('comments/', CommmentListView.as_view(), name='comments'),
    path('help-create/', HelpCreateView.as_view(), name='help-create'),
    path('helps/', HelpListView.as_view(), name='helps'),
    path('best-create/', BestCreateView.as_view(), name='best-create'),

    path('user-rating/', UsersByRatingView.as_view(), name='user-rating'),
    path('thanks/', ThanksView.as_view(), name='thanks'),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('me/', MeView.as_view()),
    path('logout/', LogoutView.as_view()),


]