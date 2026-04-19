from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Post, Category, Reaction, PollOption

# 1. Postlar ro'yxati
class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

# 2. Post tafsiloti va ko'rishlar soni
class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.views += 1  # Ko'rishlar sonini oshirish
        obj.save()
        return obj

# 3. Yangi post yaratish
class PostCreateView(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'posts/post_form.html', {'categories': categories})

    def post(self, request):
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        
        category = get_object_or_404(Category, id=category_id)
        
        post = Post.objects.create(
            author=request.user,
            category=category,
            title=title,
            content=content,
            image=image
        )
        return redirect('post_detail', pk=post.id)

# 4. Reaksiya bildirish (Like, Fire va h.k.)
class AddReactionView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        reaction_type = request.POST.get('reaction_type')
        
        reaction, created = Reaction.objects.update_or_create(
            user=request.user, 
            post=post,
            defaults={'type': reaction_type}
        )
        return redirect('post_detail', pk=post.id)

# 5. So'rovnomada ovoz berish
class PollVoteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        option = get_object_or_404(PollOption, id=pk)
        option.votes += 1
        option.save()
        return redirect('post_detail', pk=option.poll.post.id)