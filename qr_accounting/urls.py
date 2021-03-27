from django.urls import path, include
from django.conf.urls import url

from qr_accounting.views import LecturersView, ListenerView, LecturerView, qgen, bye_bye, RegisterFormView, \
    LecturersViewRun

urlpatterns = [
    # Путь на регистрацию
    url(r'^register/$', RegisterFormView.as_view(), name='register_url'),
    # Основная страница
    path('', LecturersView.as_view(), name='main_page_url'),
    path('/run', LecturersViewRun.as_view(), name='run'),
    # Добавление пути для контролера авторизации джанго
    path('', include('django.contrib.auth.urls')),
    # Путь на заявку
    path('lecture/<int:lecture_id>', LecturerView.as_view(), name='lecture'),
    # Путь на QR-код
    path('qgen/<int:lecture_id>', qgen, name='qgen'),
    # Путь на регистрацию слушателя
    path('check/<str:uuid>', ListenerView.as_view(),  name='check'),
    # Logout
    path('bye_bye/', bye_bye, name='bye_bye'),
]
