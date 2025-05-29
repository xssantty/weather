from .main import router as main_router
from .admin import router as admin_router

def register_all_handlers(dp):
    dp.include_router(main_router)
    dp.include_router(admin_router)
