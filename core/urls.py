# receipt_processor/urls.py
from django.contrib import admin
from django.urls import path
from receipts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('receipts/process', views.process_receipt, name='process_receipt'),
    path('receipts/<str:receipt_id>/points', views.get_points, name='get_points'),
]
