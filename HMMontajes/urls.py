"""
URL configuration for HMMontajes project.
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework.permissions import AllowAny

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('settlement/', include('settlement.urls')),
    path('workers/', include('workers.urls')),
    path('holidays/', include('holidays.urls')),
    path('payroll/', include('payroll.urls')),
    path('', lambda request: redirect('/workers/upload-signings'), name='index'),
    path('docs/', include_docs_urls(title='HM API', permission_classes=[AllowAny])),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
