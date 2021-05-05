from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Tag
from .forms import PostForm
from accounts.models import User
from django.contrib import messages


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

    # def get()関数 というのを継承してページにアクセスできるユーザーに制限をかける
    # requestにはurlなどの情報が入っています。
    # アクセス先のurlやメタ情報など様々な情報が含まれています。
    def get(self, request, *args, **kwargs):
      # Postオブジェクトを取得する
      # 該当のPostオブジェクトが存在しない場合HTTPのステータスが404になるのでページが存在しないことになります。
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        # 投稿したユーザーとログイン中のユーザーが一致すれば
        if self.request.user == post.user:
          # アクセスさせる
          # super()はUpdateView。
          # 親クラスは継承元のことを言うのでPostUpdateViewのことでは無い。
          # requestにはurlなどの情報が入っている。
          # アクセス先のurlやメタ情報など様々な情報が含まれている。
          # kwargsにはアクセス時に送信されたキーワード引数が含まれる。
          # こちらの解説が詳しいので参考にしてみてください
          # https://teratail.com/questions/299155
            return super().get(request, **kwargs)
        else:
          # それ以外はindexへ
            return redirect('adopt_animals:index')

class PostDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'adopt_animals/pets/post_delete.html'
    model = Post
    success_url = reverse_lazy('adopt_animals:index')

class MyPostListView(LoginRequiredMixin, ListView):
    template_name = 'adopt_animals/pets/my_post_list.html'
    model = Post
    ontext_object_name = 'post_list'
    success_url = reverse_lazy('adopt_animals:index')
    paginate_by = 8

# get_queryset(self) を使用して、ページにアクセスできるユーザーは投稿者のみにする
    def get_queryset(self):
      # Postの中でログインユーザーが投稿したもののみ表示する
        return Post.objects.filter(user_id=self.request.user.id)
  

