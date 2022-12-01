from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomAdminChangeForm
from .models import Question, CustomUser, Choice


class Register(CreateView):
    """Класс регистрации юзера"""
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class DeleteUserView(LoginRequiredMixin, DeleteView):
    """Класс удаления юзера"""
    login_url = 'login'
    model = CustomUser
    template_name = 'personal_area/delete_user.html'
    success_url = reverse_lazy('index')

    def form_valid(self):
        self.object.delete()


class UpdateUser(LoginRequiredMixin, UpdateView):
    """Класс обновления юзера"""
    login_url = 'login'
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'personal_area/update_user.html'
    success_url = reverse_lazy('personal_area')

    def get_queryset(self):
        return (super().get_queryset().filter(
            username=self.request.user
        ))

    # def dispatch(self, request, *args, **kwargs):
    #     """ Making sure that only authors can update stories """
    #     obj = self.request.user
    #     if obj != self.request.user:
    #         return redirect(obj)
    #     return super(UpdateUser, self).dispatch(request, *args, **kwargs)


class UpdateAdmin(LoginRequiredMixin, UpdateView):
    """Класс обновления дамина"""
    login_url = 'login'
    model = CustomUser
    form_class = CustomAdminChangeForm
    template_name = 'personal_area/update_admin.html'
    success_url = reverse_lazy('personal_area')


class IndexView(ListView):
    """Класс главной страницы"""
    model = Question
    paginate_by = 4
    template_name = 'index.html'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')

def handler404(request):
    response = render_to_response('404.html', {},
                              context_instance=RequestContext(request))
    response.status_code = 404
    return response


class QuestionFullView(DetailView, LoginRequiredMixin):
    """Класс подробного описания голосования"""
    model = Question
    template_name = 'questions/info_question.html'


class PersonalAreaView(LoginRequiredMixin, ListView):
    """Класс личного кабинета"""
    login_url = 'login'
    model = CustomUser
    template_name = 'personal_area/personal_area.html'


class ResultsView(DetailView, LoginRequiredMixin):
    """Класс просмотра результатов"""
    model = Question
    template_name = 'questions/results_question.html'


def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        redirect('index.html')


def logout_view(request):
    logout(request)
    redirect('index.html')


@login_required
def vote(request, question_id):
    if Question.objects.filter(id=question_id, voted_by=request.user):
        return render(request, 'vote_error.html')
    else:

        question = get_object_or_404(Question, pk=question_id)

        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            return render(request, 'questions/info_question.html', {
                'question': question,
                'error_message': 'вы не сделали выбор'
            })
        else:
            current_q = Question.objects.get(id=question_id)
            current_q.voted_by.add(request.user)
            current_q.votes += 1
            current_q.save()
            selected_choice.votes += 1
            selected_choice.save()
            return HttpResponseRedirect(reverse('result_question', args=(question.id,)))
