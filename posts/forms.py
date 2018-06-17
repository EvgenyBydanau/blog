from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
      # title = forms.ModelChoiceField(queryset=Post.objects.all().order_by("title"))
      title = forms.CharField(error_messages={'required': 'You have to fill in this filed'})
      information_correct = forms.BooleanField(required=True)

      class Meta:
          model = Post
          fields = ["title", "information_correct", "content", "image"]


      def clean(self):
          cleaned_data = super(PostForm, self).clean()
          title = cleaned_data.get('title')
          content = cleaned_data.get('content')
          if not title and not content:
              raise forms.ValidationError('You have to write something!')
          return cleaned_data


      def clean_image(self):
           image = self.cleaned_data['image']
           if image is None:
               raise forms.ValidationError('You have to upload a picture')
           return image


class CommentForm(forms.ModelForm):
     class Meta:
         model = Comment
         fields = ['content']

