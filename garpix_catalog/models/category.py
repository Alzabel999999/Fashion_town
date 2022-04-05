from django.contrib.sites.models import Site
from django.db import models
from django.conf import settings
from django.db.models import Count
from garpix_page.abstract.models.abstract_page import AbstractBasePageModel
from slugify import slugify
from ..mixins.content import OrderingMixin
from mptt.models import MPTTModel, TreeForeignKey


class CategoryManager(models.Manager):
    def get_queryset(self):
        return super(CategoryManager, self).get_queryset().annotate(
            products_count=Count('category_products')).exclude(products_count=0)


class Category(AbstractBasePageModel, OrderingMixin, MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True,
                            verbose_name='Родитель', on_delete=models.CASCADE)
    page_type = models.IntegerField(default=3, verbose_name='Тип страницы', choices=settings.CHOICES_PAGE_TYPES)

    sites = models.ManyToManyField(
        Site, verbose_name='Сайты для отображения', default=settings.SITE_ID, blank=True)

    objects = models.Manager()
    objects_with_products = CategoryManager()

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        unique_together = ['title', ]
        ordering = ('ordering', 'title',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = self.get_slug()
        super(Category, self).save(*args, **kwargs)

    def get_slug(self):
        slug = self.title
        return slugify(slug)
