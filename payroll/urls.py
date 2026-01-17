from django.urls import path
from . import views   # ✅ import the whole views module

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('new/', views.new_submission, name='new_submission'),
    path('detail/<int:submission_id>/', views.submission_detail, name='submission_detail'),
    path('export/<int:submission_id>/', views.export_submission_csv, name='export_submission_csv'),
    path('entry/<int:entry_id>/delete/', views.delete_entry, name='delete_entry'),  # ✅ delete route
    path('export-all/', views.export_all_submissions_csv, name='export_all_submissions_csv'),
]
