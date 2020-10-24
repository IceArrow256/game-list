import django.urls as DU
import registration.views as RV
import django.views.generic.base as DVGB

urlpatterns = [
    DU.path('', DU.include('django.contrib.auth.urls')),
    DU.path('sign-up', RV.SignUpView.as_view(), name='sign-up')
] 