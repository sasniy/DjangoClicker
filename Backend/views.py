from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from frontend.templates import *
from .forms import UserForm
from .models import Core, Boost  # Не забудем импортировать модель Core
from .serializers import CoreSerializer, BoostSerializer


class Register(APIView):
    def get(self, request):
        form = UserForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            core = Core(user=user)  # Создаем экземпляр класса Core и пихаем в него модель юзера
            core.save()  # Сохраняем изменения в базу
            return redirect('index')

        return render(request, 'register.html', {'form': form})


class Login(APIView):
    form = UserForm()

    def get(self, request):
        return render(request, 'login.html', {'form': self.form})

    def post(self, request):
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('index')
        return render(request, 'login.html', {'form': self.form, 'invalid': True})


@login_required
def index(request):
    core = Core.objects.get(user=request.user)
    boosts = Boost.objects.filter(core=core)  # Достаем бусты пользователя из базы
    price = core.check_level_price()
    return render(request, 'index.html', {
        'next_boost' : price,
        'core': core,
        'boosts': boosts,  # Возвращаем бусты на фронтик
    })


@api_view(['GET'])
@login_required
def call_click(request):
    core = Core.objects.get(user=request.user)
    price = core.check_level_price()
    is_levelup = core.click() # Труе если буст создался
    if is_levelup:
        Boost.objects.create(core=core, price=price*1.15, power=(core.level-1)**2) # Создание буста
    core.save()
    next_boost = core.check_level_price()
    return Response(data = { 'core': CoreSerializer(core).data, 'is_levelup': is_levelup,'next_boost':next_boost})

class BoostViewSet(viewsets.ModelViewSet):
    queryset = Boost.objects.all()
    serializer_class = BoostSerializer

    # Переопределение метода get_queryset для получения бустов, привязанных к определенному ядру
    def get_queryset(self):
        core = Core.objects.get(user=self.request.user) # Получение ядра пользователя
        boosts = Boost.objects.filter(core=core) # Получение бустов ядра
        return boosts

@api_view(['GET'])
@login_required
def buy_boost(request,pk):
    print(request)
    core = Core.objects.get(user = request.user)
    boost = Boost.objects.get(core = core,id = pk)
    buyed = False
    if boost.buy():
        buyed = True
        core.coins -= boost.price
        core.click_power += boost.power
    price = core.check_level_price()
    core.save()
    return Response({'core': CoreSerializer(core).data,'price': price,'buyed':buyed})