from django.contrib import admin
from ..models import CartItemComment, CartItemCommentPhoto, CartItemCommentVideo

class CartItemCommentPhotoInline(admin.TabularInline):
    model = CartItemCommentPhoto
    extra = 0

class CartItemCommentVideoInline(admin.TabularInline):
    model = CartItemCommentVideo
    extra = 0

@admin.register(CartItemComment)
class CartItemCommentAdmin(admin.ModelAdmin):
    inlines = (CartItemCommentPhotoInline, CartItemCommentVideoInline)
