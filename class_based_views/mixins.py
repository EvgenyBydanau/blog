from posts.models import Post


class ListMixin(object):
    def get_posts_list(self, *args, **kwargs):
        posts = Post.objects.all()
        return posts

