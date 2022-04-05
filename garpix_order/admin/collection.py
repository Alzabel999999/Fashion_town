from django.contrib import admin
from ..models import Collection, CollectionItem
from django.urls import reverse
from django.utils.html import format_html
from django.utils.html import escape, mark_safe
from django.conf import settings
from django.contrib.admin import SimpleListFilter
from garpix_catalog.models import Brand


class CollectionFilter(SimpleListFilter):
    title = 'Брэнды' # or use _('country') for translated title
    parameter_name = 'collection_brand'

    def lookups(self, request, model_admin):
        brands = set([c for c in Brand.objects.all()])
        return [(c.id, c.title) for c in brands]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(product__brand=self.value())
        else:
            return queryset


class CollectionItemInline(admin.TabularInline):

    #readonly_fields = ['order_item',]
    model = CollectionItem
    readonly_fields = ['order_item', 'link']
    #fields = ['redeemed', 'order_item', 'link']

    list_display = ['redeemed', 'order_item', 'link']
    list_display_links = ["link"]
    extra = 0
    #def order_item(self, obj):
        #return obj.order_item.name
    def link(self, obj):
        #url = reverse(...)
        #return mark_safe("<a href='%s'>edit</a>" % url)
        if obj.order_item:
            link_url = str(settings.SITE_URL) + '/admin/garpix_catalog/productsku/' + str(obj.order_item.product.id) + '/change/'
            name = str(obj.order_item.title)
            return mark_safe(f'<a href="{link_url}">{escape(name)}</a>')
            #return format_html('<a href="{}">Edit {}</a>', link, obj.user.username)
        else:
            return '-'
    link.short_description = 'Ссылка'
    link.admin_order_field = 'Ссылка' # Make row sortable
        #link_url = settings.SITE_URL + '/productsku/' + obj.order_item.product.id + '/change/'
        #name = obj.order_item.product.name
        #return u'<a href="%s">%s</a>' % (link_url , name)
        #return format_html('<a href="{}">Edit {}</a>', link, obj.user.username)

    link.allow_tags = True



@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    inlines = (CollectionItemInline, )
    list_display = ['__str__', 'status', 'product', 'get_brand', 'purchase_image']
    list_display_links = ['product', '__str__']
    readonly_fields = ['status', ]
    list_filter = (CollectionFilter, 'status')
    def get_brand(self, obj):
        return obj.product.brand.title

    def purchase_image(self, request):
        obj = request
        #order = ProductSerializer(obj, many=True).data
         #'http://91.218.229.240:8000/media/' +
        #return '<img src={0} />'.format(str(order))
        #return mark_safe('<img src={0} width="75" height="100" />'.format(url))
        try:
            url = str(request.product.get_image())
            return mark_safe('<a href="{0}" target="_blank"><img src="{0}" width="75" height="100"></a>'.format(url))
        except:
            return ''
    purchase_image.short_description = 'Превью'

    get_brand.short_description = 'Брэнд'
