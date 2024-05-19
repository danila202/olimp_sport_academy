from rest_framework import generics
from .serializers import CustomUserSerializer, ChildSerializer, ParentSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import CustomUser, Children, Parents


class CreateCustomUserView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer


class DetailCustomUserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CustomUserSerializer
    # permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(CustomUser, id=self.kwargs['pk'])


class CreateChildView(generics.CreateAPIView):
    serializer_class = ChildSerializer


class DetailChildView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChildSerializer

    def get_object(self):
        return get_object_or_404(Children, id=self.kwargs['pk'])


class CreateParentView(generics.CreateAPIView):
    serializer_class = ParentSerializer


class DetailParentView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ParentSerializer

    def get_object(self):
        return get_object_or_404(Parents, id=self.kwargs['pk'])






