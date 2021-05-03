from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Tag
from .forms import PostForm
from accounts.models import User


# Create your views here.
class IndexView(ListView):
  template_name = "index.html"
  model = Post
  context_object_name = 'post_list'
  paginate_by = 8


class CreatePostView(LoginRequiredMixin, CreateView):
  model = Post
  form_class = PostForm
  template_name = 'adopt_animals/pets/animals_post_form.html'
  success_url = reverse_lazy('adopt_animals:post_done')

# 下記のコードでPost時にユーザーを取得
# 何かformでは入力しないけど保存時に何かデータを突っ込みたいときにはdef form_valid()で入力してあげればOK
  def form_valid(self, form):
      form = form.save(commit=False)
      form.user = self.request.user
      form.save()
      return redirect('adopt_animals:post_done')

# 下記のコードでcategoryの初期値をDog（１）に設定を取得
  def get_form_kwargs(self, *args, **kwargs):
    form_kwargs = super().get_form_kwargs(*args, **kwargs)
    form_kwargs['initial'] = {'category': 1 }
    return form_kwargs

class PostDoneView(LoginRequiredMixin, TemplateView):
    template_name = 'adopt_animals/pets/post_done.html'

class PostDetailView(DetailView):
    template_name = "adopt_animals/pets/post_detail.html"
    model = Post
    context_object_name = 'post'

class PostUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'adopt_animals/pets/post_update_form.html'
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('adopt_animals:post_detail')
    context_object_name = 'post'

    # 引数が必要になる(今回の場合<pk: id)URLにリダイレクトさせる時は別途get_success_urlを継承してあげる必要があります。
    def get_success_url(self):
        return reverse('adopt_animals:post_detail', kwargs={'pk': self.object.id})
