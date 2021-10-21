from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('search_file', views.search_file, name='search_file'),
    path('clear_file', views.clear_file, name='clear_file'),
    path('get_label', views.get_label, name='get_label'),
    path('get_template', views.get_template, name='get_template'),
    path('read_data', views.read_data, name='read_data'),
    path('read_save_file', views.read_save_file, name='read_save_file'),
    path('read_file', views.read_file, name='read_file'),
    path('read_data_list', views.read_data_list, name='read_data_list'),
    path('read_label_list', views.read_label_list, name='read_label_list'),
    path('export_data', views.export_data, name='export_data'),
    path('read_z_list', views.read_z_list, name='read_z_list'),
    path('read_reconstruct_list', views.read_reconstruct_list, name='read_reconstruct_list'),
    path('reload_reconstruct', views.reload_reconstruct, name='reload_reconstruct')
]