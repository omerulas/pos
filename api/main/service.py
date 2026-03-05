import json
from django.http import HttpRequest, JsonResponse
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm, model_to_dict
from django.db.models import Model

class ApiResponse(JsonResponse):

    def __init__(self, data=None, message=None, status=200, **kwargs):
        payload = {"data": data, "message": message}
        super().__init__(data=payload, status=status, **kwargs)

class Service:
    
    def data(self, request: HttpRequest):
        return json.loads(request.body.decode('utf-8'))
    
    def login(self, request: HttpRequest):
        data = self.data(request=request)
        form = AuthenticationForm(data=data)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            return { "is_authenticated": True }
        error = "Kullanıcı adı veya şifre yanlış"
        return { "error": error}
    
    def logout(self, request):
        auth.logout(request=request)
        return {"is_authenticated": request.user.is_authenticated}
    
    def get_vn(self, model:Model):
        return model._meta.verbose_name

    def filter(self, model:Model, **kwargs):
        filtered = model.objects.filter(**kwargs)
        return filtered
    
    def instance(self, model, **kwargs):
        vn = self.get_vn(model)
        try:
            obj = model.objects.get(**kwargs)
            return obj
        except model.DoesNotExist:
            return {"error": f"{vn} bulunamadı"}
    
    def to_dict(self, model:Model, **kwargs):
        instance = self.instance(model, **kwargs)
        if not isinstance(instance, dict):
            result = model_to_dict(instance)
            return result
        return instance
    
    def serialize_qs(self, qs):
        return [model_to_dict(obj) for obj in qs]
    
    def get_first_error_message(self, form):
        for field_name, error_list in form.errors.items():
            # Eğer hata bir alana değil, formun geneline aitse (__all__)
            if field_name == '__all__':
                return error_list[0]
            
            return error_list[0]

        return "Bir hata oluştu."
        
    def save(self, model_form: ModelForm, data):
        form = model_form(data=data)
        vn = self.get_vn(model_form._meta.model)
        if form.is_valid():
            obj = form.save()
            return (f"{vn} kaydedildi", obj)
        print(form.errors)
        return {"error": self.get_first_error_message(form)}
    
    def update(self, model_form: ModelForm, data, instance):
        form = model_form(instance=instance, data=data)
        vn = self.get_vn(model_form._meta.model)
        if form.is_valid():
            form.save()
            return {"message": f"{vn} güncellendi"}
        return {"error": self.get_first_error_message(form)}
    
    def delete(self, model: Model, **kwargs):
        vn = self.get_vn(model=model)
        instance = self.instance(model, **kwargs)
        if isinstance(instance, Model):
            instance.delete()
            return {"message": f"{vn} silindi"}
        return {"error": f"{vn} bulunamadı"}
    
service = Service()