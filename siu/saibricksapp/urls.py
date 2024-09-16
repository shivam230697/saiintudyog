from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('account_list/', views.AccountList.as_view(), name="account-list"),
    path('account_update/<int:pk>', views.AccountUpdate.as_view(), name="account-update"),
    path('account_delete/<int:pk>', views.AccountDelete.as_view(), name="account-delete"),
    path('account_add/', views.AccountCreate.as_view(), name="account-add"),


]
