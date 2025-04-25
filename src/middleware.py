from fastapi import Request
from nicegui import app
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

unrestricted_page_routes = ["/login"]
admin_page_routes = ["/admin_dashboard", "/add_user", "/recon", "/recon_sendimg", "/user_training", "/training_sendimg"]
user_page_routes = ["/user_dashboard", "/recon", "/recon_sendimg"]
class AuthMiddleware(BaseHTTPMiddleware):
    """This middleware restricts access to all NiceGUI pages.

    It redirects the user to the login page if they are not authenticated.
    """
    async def dispatch(self, request: Request, call_next):
    
        if request.url.path.startswith("/_nicegui"):
            return await call_next(request)
        
        if not app.storage.user.get('authenticated') and not request.url.path in unrestricted_page_routes:
            return RedirectResponse('/login')
        
        if request.url.path in unrestricted_page_routes and bool(app.storage.user.get('role')) == False:
            return await call_next(request)
        try:
            if app.storage.user.get('role'):
                role = app.storage.user.get('role')
                if role == 1:
                    if not request.url.path in admin_page_routes:
                        return RedirectResponse("/admin_dashboard")
                    return await call_next(request)
        except:
            print("error en 1")
            print(request.headers)
            
            try:
                if role == 2:
                    if request.url.path in user_page_routes:
                        return await call_next(request)
                    return RedirectResponse("/user_dashboard")
            except:
                print("error en 2")
