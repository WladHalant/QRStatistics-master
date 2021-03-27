from django.shortcuts import redirect, render, get_object_or_404
from django.template.response import TemplateResponse

from qr_accounting.forms import LectureForm, ListenerForm
from qr_accounting.models import Lecture, Listener
from django.views.generic import View
import uuid

from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from qr_accounting.service import get_context, get_listener_context, get_lecture_context, lecture_update, get_contextRun


class RegisterFormView(FormView):
    form_class = UserCreationForm

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей
    success_url = "/"

    # Шаблон, который будет использоваться при отображении представления
    template_name = "registration/register.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно
        new_user = form.save()

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)


# Logout
def bye_bye(request):
    # Выполняем выход для пользователя, запросившего данное представление
    logout(request)

    # После чего, перенаправляем пользователя на главную страницу
    return HttpResponseRedirect("/")


# Лекции
class LecturersView(LoginRequiredMixin, View):
    # Если user неавторизованный, то переброс на страницу авторизации
    login_url = '/login/'
    raise_exception = False

    # Получение основной страницы
    def get(self, request):
        # Значения от бразузера
        user = request.user
        words = request.GET.get('words')
        page = request.GET.get('page')
        context = get_context(user, words, page)
        # Возращаем html страницу
        return TemplateResponse(request, 'qr_accounting/lectures.html', context)

    # Запись лекции в БД
    def post(self, request):
        lecturer = request.user
        # Создание заявки с инициализации полей лекции и uuid
        instance_lecture = Lecture(lecturer=lecturer, uuid=uuid.uuid1())
        # Объедение текущей формы и instance_lecture
        form_lecture = LectureForm(request.POST, instance=instance_lecture)

        # если форма валидна
        if form_lecture.is_valid():
            # Записываем форму в БД
            print("11111111111111-----------", form_lecture)
            form_lecture.save()
        else:
            print("Не прошла")
            print("11111111111111-----------", form_lecture)
            # Вывод основной страницы
            context = get_context(request.user)
            # добавление формы с ошибками
            context['errors_form_lecture'] = form_lecture
            return TemplateResponse(request, 'qr_accounting/lectures.html', context)
        return redirect('/')


class LecturersViewRun(LecturersView):
    # Получение основной страницы
    def get(self, request):
        # Значения от бразузера
        user = request.user
        words = request.GET.get('words')
        page = request.GET.get('page')
        context = get_contextRun(user, words, page)
        # Возращаем html страницу
        return TemplateResponse(request, 'qr_accounting/lectures.html', context)


# Лекция
class LecturerView(LecturersView):
    # Получение страницы "О заявке"
    def get(self, request, lecture_id, words=None):
        return TemplateResponse(request, 'qr_accounting/lecture.html', get_lecture_context(lecture_id))

    # Редактирование лекции
    def post(self, request, lecture_id):
        if request.user.groups.filter(name='executor').exists():
            return lecture_update('delete' in request.POST.get('submit_button'), request.user, request.POST or None,
                                  lecture_id, request.get_full_path())
        else:
            return render(request, 'errorPages\error_acsses.html')


# Генерация QR-кода
def qgen(request, lecture_id):
    # Присвоение лекции по id
    lecture = Lecture.objects.get(id=lecture_id)
    # Генерация uuid
    uuid_lection = str(uuid.uuid1())
    # Присвоение нового uuid
    lecture.uuid = uuid_lection
    # Обновление заявки
    lecture.save()
    context = {
        # Создание ссылки в QR-коде
        'link': 'http:/' + request.get_host() + '/check/' + uuid_lection,
        # Заявка
        'lecture': lecture,
    }
    return render(request, 'qr_accounting/qr.html', context)


# Слушатель
class ListenerView(View):
    def get(self, request, uuid):
        lecture = get_object_or_404(Lecture, uuid=uuid)
        context = {
            'topic': lecture.topic,
            'description': lecture.description,
            'form': ListenerForm()
        }
        return TemplateResponse(request, 'qr_accounting/listener.html', context)

    def post(self, request, uuid):
        return TemplateResponse(request, "qr_accounting/listener.html", get_listener_context(request.POST, uuid))
