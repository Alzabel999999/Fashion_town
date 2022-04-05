from decimal import Decimal
from django.db.models import F, Sum, Func, Count, Variance, Q
from django.db import models
from django.contrib.postgres.fields import JSONField
from slugify import slugify
from user.models import Profile
from garpix_page.abstract.mixins.content import ActiveMixin, TimeStampMixin
from garpix_catalog.mixins.content import OrderingMixin
from garpix_catalog.models import Product, ProductSku, RedemptionCondition, SizeRangePack, Minimum, Pack


class Cart(ActiveMixin, TimeStampMixin):
    profile = models.OneToOneField(
        Profile, blank=True, null=True, verbose_name='Владелец', on_delete=models.CASCADE, related_name='cart')
    session = models.CharField(max_length=255, blank=True, verbose_name='Сессия', default='')
    extra = JSONField(blank=True, verbose_name='Дополнительные данные', default=dict)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        if self.profile:
            return f'{self.profile.user}'
        else:
            return f'{self.session}'

    # @property
    def get_cart_total(self):
        items_total = self.get_selected_items().aggregate(total=Sum(F('total_price')))['total']
        packs_total = self.get_selected_packs().aggregate(total=Sum(F('total_price')))['total']
        total = Decimal('0.00')
        if items_total:
            total += items_total
        if packs_total:
            total += packs_total
        return total

    '''
    python backend/manage.py shell -c "from garpix_cart_rest.models.cart import Cart; from pprint import pprint; cart = Cart.objects.first(); rc = cart.check_conditions(); pprint(rc)"
    '''
    def check_conditions(self):
        brands = self.get_brands()
        conditions = []
        for brand in brands:
            brand_rc = brand.brand_rc
            condition = {'brand': brand, 'condition': brand_rc}
            cart_items = self.cart_items.filter(product__product__brand=brand, status=0)
            if type(brand_rc) == SizeRangePack:
                print('SizeRangePack')
            elif type(brand_rc) == Minimum:
                print('Minimum')
                if not brand_rc.one_model:
                    condition.update(self.check_minimum_for_brand(items=cart_items, rc=brand_rc, level='brand'))
                else:
                    condition.update(self.check_minimum_for_model(items=cart_items, rc=brand_rc, level='brand'))
            elif type(brand_rc) == Pack:
                print('Pack')
            else:
                print(None)
            conditions.append(condition)
        return conditions

    def get_brands(self):
        cart_items = self.cart_items.filter(
            product__product__is_in_stock=False, pack=None, status=0).select_related('product__product__brand')
        cart_packs = self.cart_packs.select_related('product__brand').filter(status=0)
        brands = []
        for item in cart_items:
            if item.product.product.brand not in brands:
                brands.append(item.product.product.brand)
        for pack in cart_packs:
            if pack.product.brand not in brands:
                brands.append(pack.product.brand)
        return brands

    def check_minimum_for_brand(self, items, rc, level='brand'):
        number = rc.number
        remain = number
        condition = {}
        # todo пока только для условия бренда (нет условий у товара и ску)
        remain -= items.aggregate(Sum('qty'))['qty__sum']
        if remain > 0:
            condition.update({'status': False, 'description': f'для выкупа не хватает {remain} товара(-ов)'})
        else:
            condition.update({'status': True, 'description': f'условие выкупа выполнено ({rc})'})
        return condition

    def check_minimum_for_model(self, items, rc, level='brand'):
        number = rc.number
        item_results = []
        for item in items:
            # todo пока только для условия бренда (нет условий у товара и ску)
            remain = number - items.filter(product__product=item.product.product).aggregate(Sum('qty'))['qty__sum']
            if remain > 0:
                item_results.append({
                    'item': item, 'status': False, 'description': f'для выкупа не хватает {remain} товара(-ов)'})
            else:
                item_results.append({
                    'item': item, 'status': True, 'description': f'условие выкупа выполнено ({rc})'})
        result = {'status': True, 'description': f'все условия выкупа выполнены ({rc})'}
        for condition in item_results:
            if not condition['status']:
                result['status'] = False
                result['description'] = 'условия выкупа не выполнены'
                if 'not_satisfying_items' in result.keys():
                    result['not_satisfying_items'].append({
                        'item': condition['item'], 'status': condition['status'], 'description': condition['description']})
                else:
                    result['not_satisfying_items'] = [{
                        'item': condition['item'], 'status': condition['status'], 'description': condition['description']}]
        return result

    def get_selected_items(self):
        return self.cart_items.filter(pack=None, selected=True, status=0).distinct()

    def get_selected_packs(self):
        return self.cart_packs.filter(selected=True, status=0)

    def get_in_cart_items(self):
        return self.cart_items.filter(pack=None, status=0).distinct()

    def get_in_cart_packs(self):
        return self.cart_packs.filter(status=0)

    def set_items_discount(self):
        items = self.get_selected_items()
        if self.profile.role == 3:
            for item in items:
                p = item.product.product
                item.price = p.wholesaller_total_price_auto
                item.old_price = p.wholesaller_price_auto if p.wholesaller_price_auto > p.wholesaller_total_price_auto else Decimal('0.00')
                item.total_item_price = p.wholesaller_total_price_auto
                item.total_price = item.total_item_price * item.qty
                #item.discount = 0
                item.save()
            return True
        elif self.profile.role == 2:
            for item in items:
                p = item.product.product
                item.price = p.dropshipper_total_price_auto
                item.old_price = p.dropshipper_price_auto if p.dropshipper_price_auto > p.dropshipper_total_price_auto else Decimal('0.00')
                item.total_item_price = p.dropshipper_total_price_auto
                item.total_price = item.total_item_price * item.qty
                #item.discount = 0
                item.save()
            return True
        else:
            discounted_items = items.filter(
                product__product__retailer_total_price_auto__lt=F('product__product__retailer_price_auto')
            )
            normal_items = items.filter(
                product__product__retailer_total_price_auto__gte=F('product__product__retailer_price_auto')
            )
            for item in discounted_items:
                p = item.product.product
                item.price = p.retailer_total_price_auto
                item.old_price = p.retailer_price_auto if p.retailer_price_auto > p.retailer_total_price_auto else Decimal('0.00')
                item.total_item_price = p.retailer_total_price_auto
                item.total_price = item.total_item_price * item.qty
                item.save()
            qty = normal_items.aggregate(total_qty=Sum('qty'))['total_qty']
            if not qty:
                qty = 0
            if qty < 3 or self.profile.role in [2, 3]:
                coeff = Decimal('1.00')
            elif qty >= 5:
                coeff = Decimal('0.90')
            else:
                coeff = Decimal('0.95')
            for item in normal_items:
                p = item.product.product
                item.price = p.retailer_total_price_auto * coeff
                item.old_price = None if coeff == Decimal('1.00') else p.retailer_total_price_auto
                item.total_item_price = p.retailer_total_price_auto * coeff
                item.total_price = p.retailer_total_price_auto * coeff * item.qty
                item.save()
            return True


    def get_total_discount(self):
        items_discount = self.get_selected_items().aggregate(discount=Sum(F('discount')))['discount']
        packs_discount = self.get_selected_packs().aggregate(discount=Sum(F('discount')))['discount']
        discount = Decimal('0.00')
        if items_discount:
            discount += items_discount
        if packs_discount:
            discount += packs_discount
        return discount

    def get_delivery(self, user):
        # todo убрать заглушки
        if user.profile.role == 3:
            return {
                'price': Decimal('0.00'),
                'description': 'ПРИ ПОЛУЧЕНИИ'
            }
        elif user.profile.role == 2:
            return {
                'price': Decimal('0.00'),
                'description': 'ПРИ УПАКОВКЕ'
            }
        else:
            return {
                'price': Decimal('0.00'),
                'description': 'ПРИ ЗАКАЗЕ'
            }

    def get_is_performed(self, brand):
        items = self.get_selected_items().filter(product__product__brand=brand)
        packs = self.get_selected_packs().filter(product__brand=brand)
        if not items and not packs:
            return False
        condition = brand.brand_rc
        if condition.rc_type == 3:
            qty = 0
            items_qty = items.aggregate(qty=Sum('qty'))['qty']
            qty += items_qty if items_qty else 0
            packs_qty = packs.aggregate(qty=Sum('total_count'))['qty']
            qty += packs_qty if packs_qty else 0
            return True if qty >= condition.number else False
        return True

    def get_is_selected(self, brand):
        items = self.get_selected_items().filter(product__product__brand=brand, selected=True).exists()
        packs = self.get_selected_packs().filter(product__brand=brand, selected=True).exists()
        return True if items or packs else False

    def select_all(self):
        self.cart_items.filter(pack=None, selected=False).update(selected=True)
        self.cart_packs.filter(selected=False).update(selected=True)
        self.save()
        return self

    def unselect_all(self):
        self.cart_items.filter(pack=None, selected=True, status=0).update(selected=False)
        self.cart_packs.filter(selected=True, status=0).update(selected=False)
        self.save()
        return self

    def check_range(self):
        pass

    def check_range_pack(self):
        pass

    def check_pack(self):
        pass
