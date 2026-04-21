


from django.urls import path
from . import views

urlpatterns = [
    path('',            views.home,             name='home'),
    path('login/',      views.login_view,       name='login'),
    path('register/',   views.register_view,    name='register'),
    path('logout/',     views.logout_view,      name='logout'),
    path('upload/',     views.upload_view,      name='upload'),
    path('materials/',  views.materials_view,   name='materials'),

    path('download/<int:material_id>/', views.download_material, name='download_material'),
    path('like/<int:material_id>/',     views.like_material,     name='like_material'),
    path('rate/<int:material_id>/',     views.rate_material,     name='rate_material'),
    path('comments/<int:material_id>/', views.get_comments,      name='get_comments'),
    path('comment/add/<int:material_id>/', views.add_comment,   name='add_comment'),
]