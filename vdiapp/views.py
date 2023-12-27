from django.db.models import Count, Sum
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView, UpdateAPIView, ListAPIView, RetrieveUpdateAPIView, \
    DestroyAPIView
from rest_framework.response import Response

from .serializers import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from .models import *


# Create your views here.

class CreateVDI(CreateAPIView):
    """
    Создание рабочего стола
    """
    serializer_class = VdiSerializer
    authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAdminUser]


class UpdateVDI(RetrieveUpdateAPIView):
    """
    Обновление рабочего стола
    """
    queryset = VirtualMachine.objects.all()
    serializer_class = VdiSerializer
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAdminUser]


class DeleteVdi(DestroyAPIView):
    """
    Удаление рабочего стола
    """
    queryset = VirtualMachine.objects.all()
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAdminUser]


class CreateHD(CreateAPIView):
    """
    Создание диска
    """
    serializer_class = HdSerializer
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAdminUser]



class UpdateHD(RetrieveUpdateAPIView):
    """
    Обновление диска
    """
    queryset = HardDrive.objects.all()
    serializer_class = HdSerializer
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAdminUser]


class CreateUser(CreateAPIView):
    """
    Создание пользователя
    """
    serializer_class = UserSerializer
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAdminUser]


class UpdateUser(RetrieveUpdateAPIView):
    """
    Обновление пользователя
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAdminUser]


class Logout(GenericAPIView):
    """
    Логоут из системы
    """
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class GetAllMachines(ListAPIView):
    """
    Получение списка всех машин
    """
    serializer_class = VdiDisplaySerializer
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAdminUser]

    def get_queryset(self):
        qs = VirtualMachine.objects.all()
        return qs


class GetAllActiveMachines(ListAPIView):
    """
    Получение списка всех активных на текущий момент машин
    """
    serializer_class = VdiDisplaySerializer
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAdminUser]

    def get_queryset(self):
        qs = VirtualMachine.objects.select_related('user', 'hd').filter(is_active=True)
        return qs


class GetAllUserMachines(ListAPIView):
    """
    Получение всех машин данного пользователя
    """
    serializer_class = VdiDisplayUserSerializer
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAdminUser]

    def get_queryset(self):
        qs = VirtualMachine.objects.filter(user=self.request.user)
        return qs


class GetAllUsers(ListAPIView):
    """
    Получение списка всех пользователей
    """
    serializer_class = UserDisplaySerializer
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAdminUser]

    def get_queryset(self):
        qs = User.objects.filter(is_staff=False)
        return qs


class VdiConnect(GenericAPIView):
    """
    Подключение к удаленному столу
    """
    serializer_class = VdiConnectSerializer
    authentication_classes = [TokenAuthentication]


    def post(self, request, *args, **kwargs):
        try:
            vdi = VirtualMachine.objects.get(user=request.user, id=kwargs['pk'], is_active=False)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            vdi.is_active = True
            vdi.save()
            return Response(status=status.HTTP_200_OK)


class VdiDisconnect(GenericAPIView):
    """
    Отключение от удаленного стола
    """
    authentication_classes = [TokenAuthentication]
    serializer_class = VdiConnectSerializer

    def post(self, request, *args, **kwargs):
        try:
            vdi = VirtualMachine.objects.get(user=request.user, id=kwargs['pk'], is_active=True)

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            vdi.is_active = False
            vdi.save()
            return Response(status=status.HTTP_200_OK)


class GetStatisic(GenericAPIView):
    """
    Получение статистики
    """
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAdminUser]

    def get_queryset(self):
        qs = VirtualMachine.objects.select_related('hd').aggregate(VDI_COUNT=Count('id'), RAM=Sum('ram'),
                                                                   CPU=Sum('cpu'), HD_VOLUME=Sum('hd__volume'))
        return qs

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()

        return Response(status=status.HTTP_200_OK, data=qs)
