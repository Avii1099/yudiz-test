from rest_framework.routers import DefaultRouter
from .views import BlogViewSet, LoginViewSet, ResetPasswordViewSet, RegisterModelView



router = DefaultRouter()

router.register(r'blog', BlogViewSet, basename="blog")
router.register(r'login', LoginViewSet, basename="login")
router.register(r'register', RegisterModelView, basename="register")
router.register(r'reset-password', ResetPasswordViewSet, basename="reset-password")


urlpatterns = router.urls