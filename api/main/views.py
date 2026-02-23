from django.views import View
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from main.service import service, ApiResponse

# Create your views here.
class App(View):
    def get(self, request):
        return HttpResponse("Backend Server")

class SessionView(View):
    """
        Handle authentication process
        HEAD    path(route="auth/csrf", view=views.Auth.as_view())
        GET     path(route="auth/check", view=views.Auth.as_view())
        POST    path(route="auth/login", view=views.Auth.as_view())
        DELETE  path(route="auth/logout", view=views.Auth.as_view())
    """
    
    @method_decorator(ensure_csrf_cookie)
    def head(self, request):
        """Set csrf"""
        return ApiResponse()
        
    def get(self, request):
        """Check auth"""
        response = service.check(request)
        user = request.user
        if user.is_authenticated and user.user_store:
            store = user.user_store.store
            response.update({"store": store.serialize()})
        return ApiResponse(data=response)
    
    def post(self, request):
        """Log in"""
        response = service.login(request)
        error = response.get("error", None)
        if error is not None:
            return ApiResponse(message=error, status=401)
        return ApiResponse(data=response)
    
    def delete(self, request):
        response = service.logout(request)
        return ApiResponse(data=response)