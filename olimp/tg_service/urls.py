from django.urls import path
from .views import CreateCustomUserView, DetailCustomUserView, CreateChildView, DetailChildView, CreateParentView, \
    DetailParentView

app_name = "tg_service"

urlpatterns = [
    path('user', CreateCustomUserView.as_view(), name='create-user'),
    path('user/<int:pk>', DetailCustomUserView.as_view(), name='detail-user'),
    path('child', CreateChildView.as_view(), name='create-child'),
    path('child/<int:pk>', DetailChildView.as_view(), name='detail-child'),
    path('parent', CreateParentView.as_view(), name='create-parent'),
    path('parent/<int:pk>', DetailParentView.as_view(), name='detail-parent'),
]