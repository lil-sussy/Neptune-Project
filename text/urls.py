from django.urls import path
from .views import SaveDocumentView, EditDocumentView, DeleteDocumentView, GetDocumentView

urlpatterns = [
    path('save_document/', SaveDocumentView.as_view(), name='save_document'),
    path('edit_document/<str:id>/', EditDocumentView.as_view(), name='edit_document'),
    path('delete_document/<str:id>/', DeleteDocumentView.as_view(), name='delete_document'),
    path('get_document/<str:id>/', GetDocumentView.as_view(), name='get_document'),
]
