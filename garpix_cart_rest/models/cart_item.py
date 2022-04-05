from decimal import Decimal
from django.db import models
from garpix_catalog.models import ProductSku
from .cart_items_pack import CartItemsPack
from .cart import Cart
from .cart_item_comment import CartItemComment


class CartItem(models.Model):

    class STATUS:
        IN_CART = 0
        ORDERED = 1
        TYPES = (
            (IN_CART, 'в корзине'),
            (ORDERED, 'заказан')
        )

    status = models.PositiveIntegerField(verbose_name='Статус', choices=STATUS.TYPES, default=STATUS.IN_CART)

    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(ProductSku, verbose_name='Товар',
                                on_delete=models.CASCADE, related_name='sku_cart_items')
    pack = models.ForeignKey(CartItemsPack, verbose_name='Упаковка', related_name='cart_pack_items',
                             blank=True, null=True, on_delete=models.CASCADE)
    comment = models.OneToOneField(CartItemComment, verbose_name='Комментарий',
                                   related_name='cart_item_comment', on_delete=models.SET_NULL, null=True, blank=True)

    change_agreement = models.BooleanField(verbose_name='Согласие на замену', default=True)

    selected = models.BooleanField(verbose_name='Выбрано', default=True)

    qty = models.IntegerField(default=1, verbose_name='Количество')

    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена', default=0.00)
    total_item_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Итоговая цена еденицы', default=0.00, blank=True, null=True)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Итоговая цена', default=0.00, blank=True, null=True)
    old_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Старая цена', default=0.00, blank=True, null=True)
    discount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Скидка', default=0.00, blank=True, null=True)

    class Meta:
        verbose_name = 'Товар корзины'
        verbose_name_plural = 'Товары корзины'
        ordering = ['-id', ]

    def __str__(self):
        return f'{self.cart} {self.product}'

    def save(self, *args, **kwargs):
        if self.pack:
            self.qty = self.pack.condition.number * self.pack.qty
        if self.qty < 1:
            self.qty = 1
        super(CartItem, self).save()
        # try:
        #     self.price, self.old_price, self.total_item_price, self.total_price = self.get_item_total()
        # except:
        #     pass
        super(CartItem, self).save()
        self.discount = self.get_discount()
        super(CartItem, self).save()

    def get_item_total(self):
        role = self.cart.profile.role
        product = self.product.product
        qty = self.qty
        if role == 3:
            auto_price = product.wholesaller_price_auto
            manual_price = product.wholesaller_price
        elif role == 2:
            auto_price = product.dropshipper_price_auto
            manual_price = product.dropshipper_price
        else:
            auto_price = product.retailer_price_auto
            manual_price = product.retailer_price
        if (not manual_price or (manual_price and manual_price >= auto_price)) and role == 1:
            price = manual_price if manual_price else auto_price
            if qty < 3:
                total_item_price = price
            elif qty >= 5:
                total_item_price = price * Decimal(0.90)
            else:
                total_item_price = price * Decimal(0.95)
            total_price = total_item_price * qty
        else:
            price = manual_price
            total_item_price = price
            total_price = price * qty
        old_price = auto_price if manual_price and manual_price < auto_price else 0.00
        return price, old_price, total_item_price, total_price

    def get_discount(self):
        total_price = self.total_price
        price = self.old_price if self.old_price else self.price
        qty = self.qty
        return (price * qty) - Decimal(total_price)

    @classmethod
    def add_item(cls, sku, cart, qty=1, role=0, pack=None):
        product = sku
        if product:
            item = cls.objects.filter(cart=cart, product=product, status=0).first()
            if item:
                item = cls.objects.create(
                    cart=cart,
                    qty=qty,
                    product=product,
                    price=product.get_price(role),
                    pack=pack,
                )
                """item.qty = item.qty + qty
                if pack:
                    item.pack = pack
                item.save()"""
                #return 'Save'
            else:
                item = cls.objects.create(
                    cart=cart,
                    qty=qty,
                    product=product,
                    price=product.get_price(role),
                    pack=pack,
                )
                #return 'Suc'
            return item
        return None

    def update_item(self, params):
        if 'qty' in params:
            self.qty = params['qty']
        if 'selected' in params:
            self.selected = params['selected']
        if 'change_agreement' in params:
            self.change_agreement = params['change_agreement']
        if 'comment' in params:
            self.comment = params['comment']
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
