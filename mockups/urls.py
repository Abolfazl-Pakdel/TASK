from django.urls import path
from .views import MockupView
from .views import MockupGenerateView,  TaskStatusView

urlpatterns = [
    path('create/', MockupView.as_view(), name='create_mockup'),
    path('generate/', MockupGenerateView.as_view(), name='mockup-generate'),
    path('tasks/<str:task_id>/', TaskStatusView.as_view(), name='task-status'),

    # path('generate/', GenerateMockupView.as_view(), name='generate-mockup'),
]

"""
from rest_framework.routers import DefaultRouter
from .views import MockupViewSet

router = DefaultRouter()
router.register(r'mockups', MockupViewSet)

urlpatterns = router.urls


"""