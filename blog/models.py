from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='Name of category')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Article(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='Name of cinema')
    content = models.TextField(verbose_name='Content of cinema')
    photo = models.ImageField(upload_to='photos/', null=True, blank=True, verbose_name='Pictures')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated')
    publish = models.BooleanField(default=True, verbose_name='Publish')
    views = models.IntegerField(default=0, verbose_name='Views')
    rating = models.FloatField(verbose_name='Rating of cinema', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Category')
    video = models.TextField(verbose_name='Add cinema', null=True, blank=True, default='')

    def get_photo(self):
        if self.photo:
            return self.photo.url
        else:
            return 'https://avatars.mds.yandex.net/i?id=2d9fbe608b16449d3b1b36d43a5aa456df181517-5419040-images-thumbs&n=13'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'