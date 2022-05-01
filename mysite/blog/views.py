from email import message
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail
from django.conf import settings

def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3) #Trzy posty na każdej stronie
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        #Jeżeli zmienna page nie jest liczbą całkowitą.
        #wówczas pobierana jest pierwsza strona wyników.
        posts = paginator.page(1)
    except EmptyPage:
        #Jeżeli zmienna page ma wartość większą niż numer ostatniej strony
        #wyników, wtedy pobierana jest ostatnia strona wyników.
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})
    
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_share(request, post_id):
    #Pobieranie posta na podstawie jego identyfikatora.
    post = get_object_or_404(Post, id=post_id, status='published')
    

    if request.method == 'POST':
        #Weryfikacja pól forumalrza zakończyła się powodzeniem.
        subject = request.POST.get('subject')
        message =  request.POST.get('message')
        email = request.POST.get('email')
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
        #...więc można wysłać wiadomość e-mail.
        return render(request, 'blog/post/share.html', {'email': email})

    return render(request, 'blog/post/share.html', {})










# Create your views here.
