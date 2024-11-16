from django.shortcuts import get_object_or_404

def like_toggle(model):
    def inner_func(func):
        def wrapper(request, *args, **kwargs):
            
            post = get_object_or_404(model, id=kwargs.get('pk'))
            user_exists = post.likes.filter(username = request.user.username).exists()
            
            if request.user != post.author:
                if user_exists:
                    post.likes.remove(request.user)
                else:
                    post.likes.add(request.user)
            
            return func(request, post)
        return wrapper
    return inner_func

