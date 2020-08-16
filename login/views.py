from django.shortcuts import render
from django.shortcuts import redirect
from .models import User
import hashlib

def hash_password(s,salt='dftba'):
    s+=salt
    h=hashlib.sha256()
    h.update(s.encode())
    return h.hexdigest()


# Create your views here.
def login(request):
    # 不允许重复登陆，再访问直接redirect到index
    if request.session.get('is_login', None):
        # 有必要设一个index（默认页面），至于映射到什么视图在路由的前面定
        return redirect('debt:index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password and username.strip():
            user = User.objects.filter(name=username)
            if len(user) == 0:
                return render(request, 'login/login.html', {'message': '没有这个用户'})
            else:
                # if user[0].password == hash_password(password):
                if user[0].password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user[0].id
                    request.session['user_name'] = user[0].name
                    request.session.set_expiry(3600)
                    return redirect('material:index')
                else:
                    return render(request, 'login/login.html', {'message': '密码错误'})
        else:
            return render(request, 'login/login.html', {'message': '请输入用户名和密码'})
    return render(request, 'login/login.html')



def logout(request):
    # 原本没有登录,现在退出
    if not request.session.get('is_login', None):
        return redirect('/login/')
    # 正常退出，删除当前的会话数据和会话cookie
    request.session.flush()
    return redirect('/login/')
