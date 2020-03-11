from rest_framework import routers
from rest_framework_extensions.routers import NestedRouterMixin

from rental import views as myapp_views



router = DynamicRouter()

router.register(r"friends", myapp_views.FriendViewset)
router.register(r"belongings", myapp_views.BelongingViewset)
router.register(r"borrowings", myapp_views.BorrowedViewset)
