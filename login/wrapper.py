from django.shortcuts import redirect


def login_required(func):
    def wrapper(*args, **kw):
        if args[0].session.get('is_login'):
            # 有返回值的要return
            # 不要忘记解包元组，形式参数要写全，否则可能wrapper() got an unexpected keyword argument 'order_id'
            return func(*args,**kw)
        else:
            return redirect('login:login')

    return wrapper
