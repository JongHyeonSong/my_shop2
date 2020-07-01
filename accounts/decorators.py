from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
        
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            """
            user와 group은 다:다 매칭으로 되어있으며
            request.user.groups.all() 은 user가 소속해있는 모든 그룹들을 리스트로 반환한다 소속그룹이 하나일경우 [0]번 인덱스로 접근한다
            """
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name #group테이블의 pk를 제외한 유일한 컬럼"name"
            
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("접근이 허가되지 않은 사용자입니다 %s만 접근하세요" % allowed_roles)
            
            return view_func(request, *args, **kwargs)
        return wrapper_func
    return decorator


def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        
        if group == 'admin':
            return view_func(request, *args, **kwargs)
        
        if group == 'customer':
            return redirect('user-page')
        
        return wrapper_func(request, *args, **kwargs)
    return wrapper_func