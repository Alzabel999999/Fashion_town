from decimal import Decimal
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from garpix_catalog.models import Product, RedemptionCondition, Color, Size
from .cart import Cart
from .cart_item_comment import CartItemComment


class CartItemsPack(models.Model):

    class STATUS:
        IN_CART = 0
        ORDERED = 1
        TYPES = (
            (IN_CART, 'в корзине'),
            (ORDERED, 'заказан')
        )

    status = models.PositiveIntegerField(verbose_name='Статус', choices=STATUS.TYPES, default=STATUS.IN_CART)

    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, related_name='cart_packs')
    product = models.ForeignKey(Product, verbose_name='Товар',
                                on_delete=models.CASCADE, related_name='product_cart_packs')
    color = models.ForeignKey(Color, verbose_name='Цвет', on_delete=models.SET_NULL, blank=True, null=True)
    size = models.ForeignKey(Size, verbose_name='Размер', on_delete=models.SET_NULL, blank=True, null=True)
    condition = models.ForeignKey(RedemptionCondition, verbose_name='Условие выкупа',
                                  on_delete=models.SET_NULL, blank=True, null=True)
    comment = models.OneToOneField(CartItemComment, verbose_name='Комментарий', related_name='cart_items_pack_comment',
                                   on_delete=models.SET_NULL, null=True, blank=True)

    selected = models.BooleanField(verbose_name='Выбрано', default=True)
    change_agreement = models.BooleanField(verbose_name='Согласие на замену', default=True)

    qty = models.IntegerField(default=1, verbose_name='Количество')
    in_pack_count = models.IntegerField(default=1, verbose_name='Количество в упаковке')
    total_count = models.IntegerField(default=1, verbose_name='Общее количество')

    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена', default=0.00)
    old_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Старая цена', default=0.00, blank=True, null=True)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Итоговая цена', default=0.00, blank=True, null=True)
    discount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Скидка', default=0.00, blank=True, null=True)

    class Meta:
        verbose_name = 'Товар корзины (в упаковке)'
        verbose_name_plural = 'Товары корзины (в упаковке)'
        ordering = ['-id',]

    def __str__(self):
        return f'{self.cart} {self.product}'

    def save(self, *args, **kwargs):
        super(CartItemsPack, self).save()
        self.condition = self.product.get_condition()
        self.in_pack_count = self.product.get_in_pack_count(self.color)
        self.total_count = self.in_pack_count * self.qty
        self.price = self.product.wholesaller_total_price_auto
        self.old_price = self.product.wholesaller_price_auto if self.product.wholesaller_price_auto > self.product.wholesaller_total_price_auto else 0
        self.total_price = Decimal(self.price) * Decimal(self.total_count)
        super(CartItemsPack, self).save()
        self.discount = self.get_discount()
        super(CartItemsPack, self).save()
        for item in self.cart_pack_items.all():
            item.save()

    @classmethod
    def add_pack(cls, pid, cart, color=None, size=None, qty=1):
        from ..models import CartItem
        from garpix_catalog.models import SizeRangePack, Pack
        product = Product.objects.filter(id=pid).first()
        if color:
            if type(color) == int:
                color = Color.objects.filter(id=color).first()
        if size:
            if type(size) == int:
                size = Size.objects.filter(id=size).first()
        if product:
            if type(product.get_condition()) == SizeRangePack:
                size = None
                skus = product.product_skus.filter(color=color)
            elif type(product.get_condition()) == Pack:
                skus = product.product_skus.filter(color=color, size=size)
            else:
                return None
            if not skus:
                return None
            pack = cls.objects.filter(product=product, color=color, size=size, status=0).first()
            if pack:
                pack.qty = pack.qty + int(qty)
                pack.save()
            else:
                pack = cls.objects.create(
                    cart=cart,
                    qty=qty,
                    product=product,
                    color=color,
                    size=size
                )
            item_ids = product.get_skus_ids_by_condition(color=color, size=size)
            items_qty = pack.condition.number * pack.qty
            for item_id in item_ids:
                cart_item = CartItem.objects.filter(product__id=item_id, pack=pack).first()
                if cart_item:
                    cart_item.qty = items_qty
                    cart_item.save()
                else:
                    sku = product.product_skus.filter(id=item_id).first()
                    CartItem.add_item(sku=sku, cart=cart, qty=items_qty, role=3, pack=pack)
            pack.save()
            return pack
        return None

    def update_items_pack(self, params):
        if 'qty' in params:
            self.qty = params['qty']
        if 'selected' in params:
            self.selected = params['selected']
        if 'change_agreement' in params:
            self.change_agreement = params['change_agreement']
        self.save()
        return None

    def add_comment(self, comment_text, files):
        if self.comment:
            comment = self.comment.update_comment(comment=comment_text, files=files)
        else:
            comment = CartItemComment.create_comment(comment=comment_text, files=files)
        self.comment = comment
        self.save()
        return comment

    def get_sizes(self):
        condition = self.product.get_condition()
        if condition.rc_type == 1:
            sizes = self.product.get_sizes(color=self.color)
            return ', '.join([s['title'] for s in sizes])
        else:
            return self.size.get_size_name()

    def get_discount(self):
        if self.old_price > self.price:
            return (self.old_price - self.price) * self.total_count
        return Decimal('0.00')
