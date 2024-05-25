from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from .models import CustomUser, Children, Parents
from .serializers import CustomUserSerializer, ChildSerializer, ParentSerializer

from datetime import time

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


class GetIdChildtView(generics.RetrieveAPIView):
    serializer_class = ChildSerializer
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_object(self):
        username = self.request.query_params.get("username")
        user = get_object_or_404(CustomUser.objects.select_related('children'),
                                 username=username, is_child=True)
        child = get_object_or_404(Children, user=user)
        return child

class GetScheduleParent(APIView):
    def get(self,request, parent_id):
        try:
            parent = Parents.objects.prefetch_related('children__subscriptions__group__schedules').get(user=parent_id)
        except Parents.DoesNotExist:
            return Response({"error": "Parent not found"}, status=status.HTTP_404_NOT_FOUND)

        schedules = []
        for child in parent.children.all():
            child_schedule = {
                "ФИО": f'{child.name} {child.surname} {child.patronymic}',
                "расписания": []
            }
            for subscription in child.subscriptions.all():
                group = subscription.group
                for gs in group.schedules.all():
                    s = gs.schedule  # Поправил gs.schedul на gs.schedule
                    child_schedule["расписания"].append({
                        "Группа": group.naming,
                        "День недели": s.day_of_week,
                        "Время начала": s.start_time,
                        "Время окончания": s.end_time
                    })
            schedules.append(child_schedule)
        return Response(data=schedules)


class GetScheduleChild(APIView):
    def get(self,request, child_id):
        try:
            child = Children.objects.prefetch_related('subscriptions'
                                         '__group__schedules').get(user=child_id)
        except Children.DoesNotExist:
            return Response({"error": "Children not found"}, status=status.HTTP_404_NOT_FOUND)

        schedules = []
        child_schedule = {
                "ФИО": f'{child.name} {child.surname} {child.patronymic}',
                "расписания": []
            }
        for subscription in child.subscriptions.all():
            group = subscription.group
            for gs in group.schedules.all():
                s = gs.schedule  # Поправил gs.schedul на gs.schedule
                child_schedule["расписания"].append({
                    "Группа": group.naming,
                    "День недели": s.day_of_week,
                    "Время начала": s.start_time,
                    "Время окончания": s.end_time
                })
        schedules.append(child_schedule)
        return Response(data=schedules)




class GetVisitationParent(APIView):
    def get(self,request, parent_id):
        try:
            parent = Parents.objects.prefetch_related('children__subscriptions').get(user=parent_id)

        except Parents.DoseNotExist:
            return Response({"error": "Parent not found"}, status=status.HTTP_404_NOT_FOUND)

        visitation = []

        for child in parent.children.all():
            visitation_dict = {
                'ФИО': f'{child.name} {child.surname} {child.patronymic}',
                'посещения': []
            }
            for subscription in child.subscriptions.all():
                for visit in subscription.visitations.all():
                    visitation_dict['посещения'].append({
                        'Дата': visit.date.strftime("%d-%m-%Y"),
                        'Время прихода': visit.time_of_arrival.strftime("%H:%M:%S")
                    })
            visitation.append(visitation_dict)

        return Response(data=visitation)


class GetVisitationChild(APIView):
    def get(self,request, child_id):
        try:
            child = Children.objects.prefetch_related('subscriptions').get(user=child_id)

        except Children.DoseNotExist:
            return Response({"error": "Children not found"}, status=status.HTTP_404_NOT_FOUND)

        visitation = []

        visitation_dict = {
            'ФИО': f'{child.name} {child.surname} {child.patronymic}',
            'посещения': []
        }
        for subscription in child.subscriptions.all():
            for visit in subscription.visitations.all():
                visitation_dict['посещения'].append({
                    'Дата': visit.date.strftime("%d-%m-%Y"),
                    'Время прихода': visit.time_of_arrival.strftime("%H:%M:%S")
                })
        visitation.append(visitation_dict)

        return Response(data=visitation)




