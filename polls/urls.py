from django.urls import path
from . import views

urlpatterns = [
    path('configure/', views.configure, name="configure"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('signup/', views.signup, name="signup"),
    path('search/', views.search, name="search"),
    path('getdataforuser/', views.getdataforuser, name="getdataforuser"),
    path('changeprofileimage/', views.changeprofileimage, name="changeprofileimage"),
    path('removeprofileimage/', views.removeprofileimage, name="removeprofileimage"),
    path('changename/', views.changename , name="changename"),
    path("changepio/", views.changepio, name="changepio"),
    path('changephone/', views.changePhone, name="changephone"),
    path('changeemail/', views.changeEmail, name="changeemail"),
    path('sendmessagewithoutfilesorimages/', views.sendmessagewithoutfilesorimages, name="sendmessagewithoutfilesorimages"),
    path('sendmessagewithfiles/', views.sendmessagewithfiles, name="sendmessagewithfiles"),
    path('sendmessagewithfiles/', views.sendmessagewithimages, name="sendmessagewithimages"),
    path('getrooms/', views.getrooms, name="getrooms"),
    path('getchat/', views.getchat, name="getchat"),
]
