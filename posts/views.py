from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from posts.models import Post, Comment
from django.views import generic
from django.urls import reverse_lazy
from posts.forms import CommentForm,PostForm


class IndexView(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=True)
    context_object_name = "posts"
    extra_context = {"title": "Главная страница"}
    template_name = "index.html"


class PostDetailView(generic.DetailView):
    model = Post
    context_object_name = "post"
    template_name = "post_detail.html"
    extra_context = {"form": CommentForm()}

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["form"] = CommentForm()
    #     return context

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            pre_saved_comment = form.save(commit=False)
            pre_saved_comment.post = post
            pre_saved_comment.save()

        return redirect("post-detail", pk)


    # def post(self, request, pk):
    #     post = Post.objects.get(pk=pk)
    #     name = request.POST.get("name", None)
    #     text = request.POST.get("text", None)
    #
    #     if name and text:
    #         comment = Comment.objects.create(name=name, text=text, post=post)
    #         comment.save()
    #
    #     return redirect("post-detail", pk)


class PostCreateView(generic.CreateView):
    model = Post
    template_name = "post_create.html"
    form_class = PostForm
    success_url = reverse_lazy("main-page")





class PostDeleteView(generic.DeleteView):
    model = Post
    success_url = reverse_lazy("main-page")


class PostUpdateView(generic.UpdateView):
    model = Post
    template_name = "post_update.html"
    success_url = reverse_lazy("main-page")
    form_class = PostForm




# def get_post(request, post_id):
#     try:
#         post = Post.objects.get(id=post_id)
#     except Post.DoesNotExist:
#         raise Http404("Такого поста нет!")
#     return render(request, "post_detail.html", {"post": post})


class AboutView(generic.TemplateView):
    template_name = "about.html"
    fields = ["title", "content"]
    success_url = reverse_lazy("about-page")

class ContactView(generic.TemplateView):
    template_name = "contacts.html"
    fields = ["title", "content"]
    success_url = reverse_lazy("contact-page")