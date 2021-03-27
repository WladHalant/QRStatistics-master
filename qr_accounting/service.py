from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.models import Group
from qr_accounting.forms import LectureForm, ListenerForm
from qr_accounting.models import Lecture, Listener
from django.shortcuts import redirect
from django.db.models import Q
import math

# Кол-во карточек
COUNT_CARDS = 6

# Генирация контекста
# Принимает сущность лектора, ключевые слова для поиска, номер страницы
def get_context(lecturer, words=None, page=1):
    # Условие, если страница передалась с пустым значение
    if not page:
        page = 1
    # Условие, если words существует
    if words:
        # Присваивание результата поиска в обратном порядке
        lectures = Lecture.objects.filter(lecturer=lecturer, topic__icontains=words.strip()).order_by('-created_at')
    else:
        # Присваивания всех лекций лектора в обратном порядке
        lectures = Lecture.objects.filter(lecturer=lecturer).order_by('-created_at')
        # lectures = Lecture.objects.order_by('-created_at')
    # Инцелизация класса
    paginator = Paginator(lectures, COUNT_CARDS)
    # Данные для генирации html
    context = {
        # Список лекций
        'lectures': paginator.page(page),
        # форма лекции
        'create_form': LectureForm(),
        # Ключевые слова, по которым был поиск
        'words': words,
        # Кол-во страниц
        'pages': range(1, math.ceil(len(lectures) / COUNT_CARDS) + 1),
    }
    return context


def get_contextRun(lecturer, words=None, page=1):
    for g in lecturer.groups.all():
        group = switch_group(g)
        if group != "null":
            break

    # Условие, если страница передалась с пустым значение
    if not page:
        page = 1
    # Условие, если words существует
    if words:
        # Присваивание результата поиска в обратном порядке
        lectures = Lecture.objects.filter(group=group, topic__icontains=words.strip()).order_by('-created_at')
    else:
        # Присваивания всех лекций лектора в обратном порядке
        lectures = Lecture.objects.filter(group=group).order_by('-created_at')
        # lectures = Lecture.objects.order_by('-created_at')
    # Инцелизация класса
    paginator = Paginator(lectures, COUNT_CARDS)
    # Данные для генирации html
    context = {
        # Список лекций
        'lectures': paginator.page(page),
        # форма лекции
        'create_form': LectureForm(),
        # Ключевые слова, по которым был поиск
        'words': words,
        # Кол-во страниц
        'pages': range(1, math.ceil(len(lectures) / COUNT_CARDS) + 1),
    }
    return context


def switch_group(x):
    print("------------------", x)
    if x.name in "Группа поддержки пользователей":
        print("++++++++++++++")
        return x
    elif x.name in 'Группа сетевых технологий':
        return x
    elif x.name in 'Группа разработки':
        return x.name
    else:
        return "null"


# Создание context для шаблона слушателя
# Принимает форму (класс), уникальное значение (строка)
def get_listener_context(listener_form, uuid):
    # Поиск заявки в БД по uuid, если нет, то 404
    lecture = get_object_or_404(Lecture, uuid=uuid)
    # Создание слушателя с инициализации поле лекции
    instance_listener = Listener(lecture=lecture)
    # Добавление в listener_form lecture
    form_listener_with_instance = ListenerForm(listener_form, instance=instance_listener)
    context = {
        # Тема заявки
        'topic': lecture.topic,
        # Описание Заявки
        'description': lecture.description,
        # Заполненная форма
        'form': form_listener_with_instance,
    }

    # Если форма валидна
    if form_listener_with_instance.is_valid():
        # Если в БД существует телефон слушателя
        if Listener.objects.filter(phone=form_listener_with_instance.cleaned_data['phone'], lecture=lecture).exists():
            # Добавление сообщение в context
            context['message_danger'] = 'Вы уже отметились на этой лекции!'
        else:
            # Если кол-во слушателей меньше зарегистрированных слушателей или кол-во слушателей равно 0
            if lecture.maximum_listeners > lecture.current_listeners or lecture.maximum_listeners == 0:
                # Сохранение слушателя из form_listener_with_instance в БД
                form_listener_with_instance.save()
                # Инкреминтируем кол-во зарегистрируемых слушателей
                lecture.current_listeners += 1
                # Обновляем заявку в БД
                lecture.save()
                context['message_successful'] = 'Удачно прослушать лекцию!'
            else:
                context['message_danger'] = 'Регистрация закончилась'
    return context


# Возращает context для лекции
def get_lecture_context(lecture):
    # Слушатели
    listeners = Listener.objects.filter(lecture=lecture)
    # Поиск заявки в БД по id, если нет, то 404
    lecture = get_object_or_404(Lecture, id=lecture)

    context = {
        # Слушатели
        'listeners': listeners,
        # Заявка
        'lecture': lecture,
        # Создание форм
        'update_form': LectureForm(instance=lecture),
        'create_form': LectureForm(),

    }
    return context


# Обновление лекции
def lecture_update(submit_button, lecturer, form, lecture, path):
    # Если нажата кнопка
    if submit_button:
        # Достаем заявку, которая удалиться
        lecture = Lecture.objects.filter(id=lecture, lecturer=lecturer)
        # Если заявка существует
        if lecture.exists():
            # Удаление заявки
            lecture.delete()
        # Возвращение на основную страницу
        response = redirect('/')
    else:
        # Поиск заявки в БД по id, если нет, то 404
        instance = get_object_or_404(Lecture, id=lecture)
        # Создаем форму лекции + id
        form_lecture = LectureForm(form, instance=instance)
        # Если форма валидна
        if form_lecture.is_valid():
            # Обнавление формы в БД
            form_lecture.save()
        # Возращение на текущую заявку
        # response = redirect(path)
        response = redirect('/')
    return response
