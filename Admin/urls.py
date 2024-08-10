from django.contrib import admin
from django.urls import path
from myadmin import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.loginView, name='loginView'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('service-provider/', views.service_provider, name='service-provider'),
    path('add-invoice/', views.add_invoice, name='add-invoice'),
    path('add-services/', views.add_services, name='add-services'),
    path('report/', views.report, name='report'),  # Adjust the view function name as needed
    path('generate-pdf/', views.generate_pdf, name='generate-pdf'),
    path('review-invoice/',views.review_invoice,name='review-invoice'),
    path('company/edit/<int:id>/', views.edit_company, name='edit_company'),
    path('edit-client/<int:id>/', views.edit_client, name='edit-client'),
    path('delete_company/<int:id>/', views.delete_company, name='delete_company'),
    path('gst-report/<int:client_id>/', views.gst_report, name='gst-report'),
    path('client/<int:client_id>/', views.show_client, name='show-client'),  # Updated parameter name to 'client_id'
    path('client/<int:client_id>/delete/', views.delete_client, name='delete-client'),  # Updated parameter name to 'client_id'
]

