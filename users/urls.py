from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path
from . import views
from .views import Register, PersonalAreaView, DeleteUserView, UpdateUser, IndexView, \
    QuestionFullView, UpdateAdmin

urlpatterns = [
    path('', IndexView.as_view(template_name="index.html"), name='index'),
    path('signup/', Register.as_view(), name='signup'),
    path('personal_area/', PersonalAreaView.as_view(), name='personal_area'),
    path('delete_user/<int:pk>/', DeleteUserView.as_view(), name='delete_user'),
    path('update_user/<int:pk>/', UpdateUser.as_view(), name='update_user'),
    path('update_admin/<int:pk>/', staff_member_required(login_url='login')(UpdateAdmin.as_view()), name='update_admin'),
    path('question_info/<int:pk>/', QuestionFullView.as_view(), name='info_question'),
    path('vote/<int:question_id>/', views.vote, name='vote'),
    path('result/<int:pk>/', views.ResultsView.as_view(), name='result_question'),
]