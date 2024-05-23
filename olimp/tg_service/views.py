from rest_framework import generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from .models import CustomUser, Children, Parents
from .serializers import CustomUserSerializer, ChildSerializer, ParentSerializer


class CreateCustomUserView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer


class DetailCustomUserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CustomUserSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

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



class GetIdUserView(generics.RetrieveAPIView):
    serializer_class = CustomUserSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        username = self.request.query_params.get("username")
        user = get_object_or_404(CustomUser, username=username)
        return user

class GetIdParentView(generics.RetrieveAPIView):
    serializer_class = ParentSerializer
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_object(self):
        username = self.request.query_params.get("username")
        user = get_object_or_404(CustomUser.objects.select_related('parent'),
                                 username=username, is_parent=True)
        parent = get_object_or_404(Parents, user=user)
        return parent




