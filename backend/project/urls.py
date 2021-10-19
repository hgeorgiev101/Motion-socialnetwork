"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt import views as jwt_views

from project import settings
from user.views import ListAllUsersView, RetrieveUpdateProfileView, CustomTokenObtainPairView
from user.views import SpecificUserView

schema_view = get_schema_view(
    openapi.Info(
        title="Motion Project API",
        default_version='v0.1',
        description="Motion Social Media App API",
    ),
    public=True,  # Set to False restrict access to protected endpoints
    permission_classes=(permissions.AllowAny,),  # Permissions for docs access
)

urlpatterns = [
    path('backend/admin/', admin.site.urls),
    path('backend/api/social/posts/', include('post.urls')),
    path('backend/api/users/', ListAllUsersView.as_view()),
    path('backend/api/users/<int:user_id>/', SpecificUserView.as_view()),
    path('backend/api/users/me/', RetrieveUpdateProfileView.as_view()),
    path('backend/api/social/followers/', include('user.urls')),
    path('backend/api/auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('backend/api/auth/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('backend/api/auth/token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_refresh'),
    path('backend/api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('backend/api/auth/', include('registration_profile.urls')),
    path('backend/api/social/comments/', include('comment.urls')),

    path('backend/api/friends/', include('friend_request.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
