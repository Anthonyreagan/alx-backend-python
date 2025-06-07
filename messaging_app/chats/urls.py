from django.urls import path, include
from rest_framework_extensions.routers import ExtendedDefaultRouter
from .views import ConversationViewSet, MessageViewSet

router = ExtendedDefaultRouter()

# Parent router (conversations)
conversation_route = router.register(
    r'conversations',
    ConversationViewSet,
    basename='conversations'
)

# Nested router (messages under conversations)
conversation_route.register(
    r'messages',
    MessageViewSet,
    basename='conversation-messages',
    parents_query_lookups=['conversation']
)

urlpatterns = [
    path('', include(router.urls)),
]