'''
python manage.py shell -c "from utils.create_test_data import filling_db; filling_db()"
python backend/manage.py shell -c "from utils.create_test_data import filling_db; filling_db(5)"
python manage.py shell -c "from utils.create_test_data import clear_db; clear_db()"
'''
from .test_data import brand_list, categories, colors_list, delivery_method_list, payment_methods_list, users_list
from garpix_cart_rest.models.cart_item import CartItem
from garpix_cart_rest.models.cart import Cart
from garpix_catalog.models.redemption_condition import RedemptionCondition, SizeRangePack, Pack, Minimum
from garpix_catalog.models.product_sku import ProductSku
from garpix_catalog.models.category import Category
from garpix_catalog.models.product import Product
from garpix_catalog.models.brand import Brand
from garpix_catalog.models.size import Size
from garpix_catalog.models.color import Color
from garpix_catalog.models.live_photo_album import LivePhotoAlbum
from garpix_catalog.models.brand_category import BrandCategory
from garpix_order.models.delivery_address import DeliveryAddress
from garpix_order.models.delivery_method import DeliveryMethod
from garpix_order.models.payment_method import PaymentMethod
from garpix_order.models import Requisites
from garpix_order.models import OrderItem
from garpix_order.models import Order
from content.models import Announce
from content.models import Review
from content.models import Likes
from content.models import News
from django.conf import settings
from user.models import User, Payment
import random

random.seed()


def clear_db():
    try:
        clear_users()
        clear_conditions_db()
        clear_category_db()
        clear_brands_db()
        clear_brand_category()
        clear_product_db()
        clear_color_db()
        clear_product_scu_db()
        clear_live_photo_album_db()
        clear_cart()
        clear_cart_items()
        clear_delivery_address()
        clear_delivery_method()
        clear_payment_method()
        clear_requisites()
        clear_order()
        clear_order_item()
        clear_news()
        clear_announce()
        clear_reviews()
        clear_payments()
    except Exception as e:
        print(str(e))


def filling_db(count=5):
    create_users()
    brand_conditions = create_conditions()
    create_category()
    create_brands(brand_conditions)
    create_brand_category()
    create_products()
    create_size()
    create_color()
    create_product_scu()
    create_live_photo_album()
    create_cart()
    create_cart_items()
    create_delivery_address()
    create_delivery_method()
    create_payment_method()
    create_requisites()
    create_order()
    create_order_item()
    create_news()
    create_announce()
    create_reviews()
    create_payments()


def create_users():
    try:
        for item in users_list:
            username = item['login']
            first_name = item['first_name']
            last_name = item['last_name']
            email = item['e-mail']
            user = User(username=username, first_name=first_name,
                        last_name=last_name, email=email)
            print(username)
            user.save()
            user.profile.role = item['role']
            user.set_password(item['password'])
    except Exception as e:
        print(str(e))


def create_conditions():
    conditions = {
        0: {'order_type': Minimum, 'number': 1, 'one_model': False},
        2: {'order_type': Minimum, 'number': 3, 'one_model': False},
        3: {'order_type': Minimum, 'number': 5, 'one_model': False},
        4: {'order_type': Minimum, 'number': 2, 'one_model': True},
        5: {'order_type': Minimum, 'number': 10, 'one_model': False},
        6: {'order_type': Pack, 'number': 4},
        7: {'order_type': Pack, 'number': 6},
        8: {'order_type': SizeRangePack, 'number': 2},
        9: {'order_type': SizeRangePack, 'number': 3},
        10: {'order_type': Minimum, 'number': 5, 'one_model': False},
    }
    conditions_dict = {}
    for k, v in conditions.items():
        if v['order_type'] == Minimum:
            rc = v['order_type'](number=v['number'], one_model=v['one_model'])
            rc.save()
            conditions_dict[k] = rc
        elif v['order_type'] == Pack:
            rc = v['order_type'](number=v['number'])
            rc.save()
            conditions_dict[k] = rc
        elif v['order_type'] == SizeRangePack:
            rc = v['order_type'](number=v['number'])
            rc.save()
            conditions_dict[k] = rc
        else:
            rc = v['order_type'](number=1, one_model=False)
            rc.save()
            conditions_dict[k] = rc
    return conditions_dict


def create_brands(brand_conditions):
    for k, v in brand_list.items():
        try:
            brand = Brand.objects.create(title=k, brand_rc=brand_conditions[v])
            print('Бренд:', brand)
        except Exception as e:
            print(str(e))


def create_category():
    for k, v in categories.items():
        parent = Category.objects.filter(title=v['parent']).first()
        category = Category.objects.create(title=k, parent=parent)
        print(f'Категория: {category}')
        category.sites.set([1])
        category.save()


def create_brand_category(count=2):
    all_brands = Brand.objects.all()
    all_categories = Category.objects.all()
    for brand_item in all_brands:
        cat_count = random.choice(range(count)) + 1
        for i in range(cat_count):
            brand_title = Brand.objects.filter(title=brand_item).first()
            category_title = Category.objects.filter(title=random.choice(all_categories)).first()
            markup_for_wholesaller = random.choice(range(0, 100))
            markup_for_wholesaller_type = random.choice((1, 2))
            markup_for_dropshipper = random.choice(range(0, 150))
            markup_for_retailer = random.choice(range(0, 200))
            try:
                brand_category = BrandCategory.objects.create(
                    category=category_title, brand=brand_title, markup_for_wholesaller=markup_for_wholesaller,
                    markup_for_wholesaller_type=markup_for_wholesaller_type,
                    markup_for_dropshipper=markup_for_dropshipper,
                    markup_for_retailer=markup_for_retailer,
                )
                print('Brand Category:', brand_category)
            except Exception as e:
                print(str(e))


def create_products(count=5):
    for brand_category in BrandCategory.objects.all():
        category = brand_category.category
        category_dict = categories[category.title]
        for product_type in category_dict['product_list']:
            product_count = random.choice(range(1, count))
            for i in range(product_count):
                product_title = f'{product_type} {str(i + 1)}'
                product_weight = random.choice([i for i in range(1, 20)]) / 10
                purchase_price = random.choice(range(1, 100))
                product_rc = None
                product = Product.objects.create(
                    title=product_title,
                    weight=product_weight, purchase_price=purchase_price,
                    brand_category=brand_category, product_rc=product_rc
                )
                print(f'Продукт: {product_title}')
                product.sites.set([1])
                product.save()


'''
python backend/manage.py shell -c "from utils.create_test_data import create_size; create_size()"
'''
def create_size():
    for i in range(11):
        try:
            size = Size.objects.create(size=i)
            print('Размер:', size)
        except Exception as e:
            print(str(e))

'''
python backend/manage.py shell -c "from utils.create_test_data import create_color; create_color()"
'''
def create_color():
    for k, v in colors_list.items():
        try:
            color = Color.objects.create(title=k, color=v)
            print('Цвет:', color)
        except Exception as e:
            print(str(e))


'''
python backend/manage.py shell -c "from utils.create_test_data import create_product_scu; create_product_scu()"
'''
def create_product_scu(count=5):
    all_products = Product.objects.all()
    all_colors = Color.objects.all()
    all_sizes = Size.objects.all()
    for product in all_products:
        sku_count = random.choice(range(count)) + 1
        for i in range(sku_count):
            try:
                size=random.choice(all_sizes)
                color = random.choice(all_colors)
                in_stock_count = random.choice([i for i in range(0, 3)])
                product_scu = ProductSku.objects.create(
                    product=product, size=size, color=color,
                    in_stock_count=in_stock_count
                )
                print('Продукт SCU:', product)
                product_scu.sites.set([1])
                product_scu.save()
            except Exception as e:
                print(str(e))


def create_live_photo_album():
    for category in categories.keys():
        try:
            live_photo_album_title = category
            brand = Brand.objects.filter(title=random.choice(list(brand_list.items()))[0]).first()
            live_photo_album = LivePhotoAlbum.objects.create(
                title=live_photo_album_title, brand=brand
            )
            print('Альбом живых фото:', live_photo_album, brand)
            live_photo_album.sites.set([1])
            live_photo_album.save()
        except Exception as e:
            print(str(e))


def create_cart():
    all_users = User.objects.all()
    for user in all_users:
        try:
            cart = Cart.objects.create(user=user)
            print('Корзина пользователя:', user, cart)
        except Exception as e:
            print(str(e))


def create_cart_items(count=10):
    all_product = Product.objects.all()
    all_cart = Cart.objects.all()
    for cart in all_cart:
        products_count = random.choice(range(count))
        for i in range(products_count):
            try:
                random_product = random.choice(all_product)
                random_sku = random.choice(random_product.product_skus.all())
                qty = random.choice(range(count))
                price = random_sku.get_price()
                cart_item = CartItem.objects.create(
                    price=price, qty=qty, product=random_sku, cart_id=cart.id
                )
                print('Корзина:', random_sku, cart_item)
            except Exception as e:
                print(str(e))


def create_delivery_method():
    d = 0
    try:
        while d <= 4:
            for delivery in delivery_method_list:
                delivery_types_all = [i for i in settings.CHOICE_DELIVERY_TYPES]
                delivery_type = delivery_types_all[d][0]
                d += 1
                delivery_method = DeliveryMethod.objects.create(
                    title=delivery, type=delivery_type
                )
                print('Метод доставки:', delivery_type, delivery_method)
    except Exception as e:
        print(str(e))


def create_payment_method():
    d = 0
    try:
        while d <= 1:
            for pay in payment_methods_list:
                payment_types_all = [i for i in settings.CHOICE_PAYMENT_TYPES]
                payment_type = payment_types_all[d][0]
                d += 1
                payment_method = PaymentMethod.objects.create(title=pay, type=payment_type)
                print('Метод оплаты:', payment_type, payment_method)
    except Exception as e:
        print(str(e))


def create_delivery_address():
    all_users = User.objects.all()
    for user in all_users:
        try:
            delivery_address = DeliveryAddress.objects.create(
                profile=user.profile, post_code=123456, country=random.choice(DeliveryAddress.COUNTRY.TYPES)[0],
                city='Some city', street='Some street',
                house=random.choice(range(200)), flat=random.choice(range(200))
            )
            print('Aдреc доставки пользователя', user, delivery_address)
        except Exception as e:
            print(str(e))


def create_requisites(count=5):
    for i in range(count):
        try:
            requisites_text = 'Some requisites'
            requisites = Requisites.objects.create(requisites=requisites_text)
            print('Реквизиты:', requisites)
        except Exception as e:
            print(str(e))

'''
python backend/manage.py shell -c "from utils.create_test_data import create_order; create_order()"
'''
def create_order(count=20):
    all_carts = Cart.objects.all()
    all_delivery_methods = DeliveryMethod.objects.all()
    all_payment_methods = PaymentMethod.objects.all()
    all_requisites = Requisites.objects.all()
    for cart in all_carts:
        profile = cart.profile
        orders_count = random.choice(range(count))
        delivery_address = DeliveryAddress.objects.filter(profile=profile).first()
        for i in range(orders_count):
            try:
                delivery_method = random.choice(all_delivery_methods)
                payment_method = random.choice(all_payment_methods)
                requisites = random.choice(all_requisites)
                order = Order.objects.create(
                    profile=profile, cart=cart,
                    delivery_method=delivery_method, delivery_address=delivery_address,
                    payment_method=payment_method, requisites=requisites)
                print('Заказ пользователя', profile, order)
            except Exception as e:
                print(str(e))

'''
python backend/manage.py shell -c "from utils.create_test_data import create_order_item; create_order_item(10)"
'''
def create_order_item(count=10):
    all_orders = Order.objects.all()
    all_product = ProductSku.objects.all()
    for order in all_orders:
        order_items_count = random.choice(range(count))
        for i in range(order_items_count):
            try:
                title = 'Random order item'
                price = random.choice(range(50, 300))
                qty = random.choice(range(1, 10))
                product = random.choice(all_product)
                order_item = OrderItem.objects.create(
                    order=order, title=title, price=price, qty=qty, product=product
                )
                print('Order item:', title, order_item)
            except Exception as e:
                print(str(e))


def create_news(count=30):
    for i in range(count):
        title = f'Новость {str(i + 1)}'
        description = 'Random description'
        is_for_retailer = random.choice([True, False])
        is_for_wholesaler = random.choice([True, False])
        is_for_dropshipper = random.choice([True, False])
        news = News.objects.create(
            title=title, description=description, is_for_retailer=is_for_retailer,
            is_for_wholesaler=is_for_wholesaler, is_for_dropshipper=is_for_dropshipper
        )
        print('News', title, news)
        news.sites.set([1])
        news.save()


def create_announce(count=5):
    for i in range(count + 1):
        url = '/'
        content = 'Содержимое анонса'
        announce = Announce.objects.create(url=url, content=content)
        print('Announce', content)


def create_reviews(count=5):
    all_users = User.objects.all().exclude(is_superuser=True)
    all_product = Product.objects.all()
    for i in range(count * 100 + 1):
        product = random.choice(all_product)
        product_choices = [None, product, product]
        profile = random.choice(all_users).profile
        stars = random.choice(range(1, 6))
        content = 'Some review content'
        review = Review.objects.create(
            profile=profile, product=random.choice(product_choices),
            stars=stars, content=content
        )
        print(f'Обзор на товар {product} пользователя {profile}')
        random_count = random.choice(range(0, len(all_users)))
        for j in range(random_count):
            try:
                liked_profile = random.choice(all_users).profile
                is_active = random.choice([True, False])
                like = Likes(profile=liked_profile, review=review, is_active=is_active)
                like.save()
            except Exception as e:
                print(str(e))


'''
python backend/manage.py shell -c "from utils.create_test_data import create_payments; create_payments()"
'''
def create_payments():
    users = User.objects.all()
    try:
        for user in users:
            orders = Order.objects.filter(profile=user.profile)
            for order in orders:
                status = random.choice([0,1,2])
                if status in [0,1]:
                    Payment.objects.create(
                        profile=user.profile,
                        order=order,
                        status=status,
                        comment='',
                        cost=order.get_order_total(),
                    )
    except Exception as e:
        print(str(e))


def clear_live_photo_album_db():
    LivePhotoAlbum.objects.all().delete()


'''
python backend/manage.py shell -c "from utils.create_test_data import clear_delivery_address; clear_delivery_address()"
'''
def clear_delivery_address():
    DeliveryAddress.objects.all().delete()


def clear_delivery_method():
    DeliveryMethod.objects.all().delete()


def clear_brand_category():
    BrandCategory.objects.all().delete()


def clear_payment_method():
    PaymentMethod.objects.all().delete()


def clear_product_scu_db():
    ProductSku.objects.all().delete()


'''
python backend/manage.py shell -c "from utils.create_test_data import clear_conditions_db; clear_conditions_db()"
'''
def clear_conditions_db():
    Minimum.objects.all().delete()
    SizeRangePack.objects.all().delete()
    Pack.objects.all().delete()


def clear_cart_items():
    CartItem.objects.all().delete()


def clear_category_db():
    Category.objects.all().delete()


def clear_order_item():
    OrderItem.objects.all().delete()


def clear_requisites():
    Requisites.objects.all().delete()


def clear_product_db():
    Product.objects.all().delete()


def clear_brands_db():
    Brand.objects.all().delete()


def clear_announce():
    Announce.objects.all().delete()


def clear_color_db():
    Color.objects.all().delete()


def clear_reviews():
    Review.objects.all().delete()


def clear_users():
    User.objects.all().exclude(is_superuser=True).delete()


def clear_order():
    Order.objects.all().delete()


def clear_news():
    News.objects.all().delete()


def clear_cart():
    Cart.objects.all().delete()


def clear_payments():
    Payment.objects.all().delete()
