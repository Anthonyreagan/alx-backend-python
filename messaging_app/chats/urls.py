from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet
from rest_framework_extensions.routers import NestedDefaultRouter  # Add this import


# Create a router and register our viewsets
router = routers.DefaultRouter()

router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

nested_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
nested_router.register(r'messages', MessageViewSet, basename='conversation-messages')
# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]