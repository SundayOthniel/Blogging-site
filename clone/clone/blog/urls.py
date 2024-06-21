from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.BloggerLogin.as_view(), name='blogger_signin'),
    path('signup', views.BloggerSignupView.as_view(), name='blogger_signup'),
    path('blogger_login', views.BloggerLogin.as_view(), name='blogger_login'),
    path('password-reset', views.PasswordReset.as_view(), name='password_reset'),
    path('link-sent', views.LinkSent.as_view(), name='link_sent'),
    path('blogger-dashboard',views.BloggerDashboard.as_view(), name='blogger_dashboard'),
    path('blogger_profile', views.BloggerProfile.as_view(), name='blogger_profile'),
    path('blogger-edit-profile', views.BloggerEditProfile.as_view(), name='blogger_edit_profile'),
    path('create-content', views.CreateContent.as_view(), name='create_content'),
] 

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)