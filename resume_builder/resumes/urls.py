from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_resume, name='create_resume'),
    path('preview/<uuid:uuid>/', views.preview_resume, name='preview_resume'),
    path('payment-success/<uuid:uuid>/', views.payment_success, name='payment_success'),
    path('download/<uuid:uuid>/', views.download_pdf, name='download_pdf'),
]