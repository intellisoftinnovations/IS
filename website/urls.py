from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('about/', views.about, name='about'),
    path('process/', views.process, name='process'),
    path('contact/', views.contact, name='contact'),
    path('contact/success/', views.contact_success, name='contact_success'),

    # Direct preview endpoints for testing custom error pages
    path('400/', views.error_400, name='preview_400'),
    path('403/', views.error_403, name='preview_403'),
    path('404/', views.error_404, name='preview_404'),
    path('500/', views.error_500, name='preview_500'),

    # Unmatched route catch-all (handles URLs like /serv with custom branded 404, excluding media/, static/, and admin)
    re_path(r'^(?!media/|static/|admin(?:/|$)).*$', views.error_404, name='catch_all_404'),
]
