from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from arango import views

urlpatterns = [
    # session URL'S
    path('', views.HomeView.as_view()),
    path('init/', views.Initialize.as_view()),
    path('provider/', csrf_exempt(views.Provider.as_view())),
    path('service-area/', csrf_exempt(views.ServiceArea.as_view())),
]
