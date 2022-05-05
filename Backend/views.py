from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import redirect, render
from rest_framework import request
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import UserForm


class UserApi(APIView):
    def get(self, request):
        id = request.query_params.get("id")  # Получение id из параметров запроса
        if User.objects.filter(id=id).exists():
            print(request.user)
            user = User.objects.get(pk=id)
            return Response({
                "id": user.id,
                "username": user.username,
            })
            # Получаем пользователя
        # Если в запросе нет параметра id, возвращаем все заметки
        return Response({
            "error": "Пользователя с таким id не найдено"
        })

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        new_user = User.objects.create_user(username=username, password=password)
        return Response({'user': model_to_dict(new_user)})


def index(request):
    return render(request, 'index.html')
