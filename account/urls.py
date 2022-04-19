from django.urls import path
from account.views import ChangePassword, UserRegisterView, UserLoginView ,CurrentUserView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name="register"),
    path('login/', UserLoginView.as_view() ,name="login"),
    path('currentuser/', CurrentUserView.as_view() ,name="current_user"),
    path('changepassword/', ChangePassword.as_view() ,name="change_password")

]   
