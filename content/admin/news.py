from django.contrib import admin
from ..models import News, NewsPhoto, NewsVideo, NewsRubric
from django.contrib.admin import SimpleListFilter


class RubricFilter(SimpleListFilter):
    title = 'Рубрики' # or use _('country') for translated title
    parameter_name = 'news'

    def lookups(self, request, model_admin):
        allmat = set([c for c in NewsRubric.objects.all()])
        return [(c.id, c.title) for c in allmat]
        #return set([c.title for c in NewsRubric.objects.all()])

    def queryset(self, request, queryset):
        if self.value():
            rubric = NewsRubric.objects.get(id=self.value())
            #return queryset
            return queryset.filter(rubrics=rubric)
        else:
            return queryset

class NewsPhotoInline(admin.TabularInline):
    model = NewsPhoto
    extra = 0


class NewsVideoInline(admin.TabularInline):
    model = NewsVideo
    extra = 0


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_for_retailer', 'is_for_wholesaler', 'is_for_dropshipper', 'get_rubric']
    fieldsets = (
        (None, {'fields': ('is_active', 'title', 'slug', 'description',
                           'content', 'image', 'image_thumb', 'rubrics',
                           'is_for_retailer', 'is_for_wholesaler', 'is_for_dropshipper', 'parent',)}),
        ('SEO', {'fields': ('seo_title', 'seo_keywords', 'seo_description', 'seo_author',
                            'seo_og_type', 'seo_image',), 'classes': ('tabed',)})
    )
    readonly_fields = ('slug', 'image_thumb',)
    inlines = [NewsPhotoInline, NewsVideoInline]
    list_filter = (RubricFilter,)
    #list_filter = ('news__rubrics__title',)

    def get_rubric(self, obj):
        try:
            allmat = set([c for c in obj.rubrics.all()])
            return [(c.title) for c in allmat]
        except:
            return '-'
    get_rubric.short_description = 'Рубрики'
