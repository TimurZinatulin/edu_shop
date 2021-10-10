# complete
from . import views
from django.urls import path

app_name = 'dadova'
urlpatterns = [
	path('', views.home, name='home'),
	path('features/', views.features, name='features'),
	path('categories/', views.categories, name='categories'),
	path('courses/<int:cat_id>/', views.courses, name='courses'),
	path('<int:cour_id>/', views.detail, name='detail'),
	path('<int:cour_id>/<int:user_id>/leave_review/', views.leave_review, name='leave_review'),
	path('events/', views.events, name='events'),
	path('register/', views.register, name='register'),
	path('login/', views.user_login, name='user_login'),
	path('cart/<int:user_id>/', views.cart, name='cart'),
	path('<int:cour_id>/<int:user_id>/add_to_cart/', views.add_to_cart, name='add_to_cart'),
	path('profile/<int:user_id>/', views.profile, name='profile'),
	path('<int:cour_id>/<int:user_id>/buy/', views.buy, name='buy'),
]