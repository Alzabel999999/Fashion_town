'''
python backend/manage.py shell -c "from utils.some_scripts import resave_products; resave_products()"
'''
def resave_products():
    from garpix_catalog.models import Product
    try:
        products = Product.objects.all()
        for p in products:
            p.save()
        print('update_models_total_prices() - done')
    except Exception as e:
        print('update_models_total_prices() - error:', str(e))


'''
python backend/manage.py shell -c "from utils.some_scripts import resave_products_with_images; resave_products_with_images()"
'''
def resave_products_with_images():
    from garpix_catalog.models import Product
    from garpix_page.models import Page
    from django.core.files import File
    from django.conf import settings
    import random
    import os

    directory = os.path.join(settings.BASE_DIR, 'utils', 'images')
    files = os.listdir(directory)

    try:
        products = Product.objects.all()
        for p in products:
            if not p.image:
                image_name = random.choice(files)
                image_path = os.path.join(directory, image_name)
                with open(image_path, 'rb') as f:
                    p.image.save(image_name, File(f), save=True)
                    f.close()
            if not p.parent:
                p.parent = Page.objects.filter(page_type=settings.PAGE_TYPE_CATALOG).first()
                p.save()
        print('resave_products_with_images() - done')
    except Exception as e:
        print('resave_products_with_images() - error:', str(e))


'''
python backend/manage.py shell -c "from utils.some_scripts import resave_skus_with_images; resave_skus_with_images()"
'''
def resave_skus_with_images():
    from garpix_catalog.models import ProductSku
    from django.core.files import File
    from django.conf import settings
    import random
    import os

    directory = os.path.join(settings.BASE_DIR, 'utils', 'images')
    files = os.listdir(directory)

    try:
        products = ProductSku.objects.all()
        for p in products:
            if not p.image:
                image_name = random.choice(files)
                image_path = os.path.join(directory, image_name)
                with open(image_path, 'rb') as f:
                    p.image.save(image_name, File(f), save=True)
                    f.close()
        print('resave_skus_with_images() - done')
    except Exception as e:
        print('resave_skus_with_images() - error:', str(e))


'''
python backend/manage.py shell -c "from utils.some_scripts import resave_cart_items; resave_cart_items()"
'''
def resave_cart_items():
    from garpix_cart_rest.models import CartItem
    try:
        items = CartItem.objects.all()
        for p in items:
            print(p.id)
            p.save()
        print('update_models_total_prices() - done')
    except Exception as e:
        print('update_models_total_prices() - error:', str(e))


'''
python backend/manage.py shell -c "from utils.some_scripts import fix_empty_colors_and_sizes; fix_empty_colors_and_sizes()"
'''
def fix_empty_colors_and_sizes():
    from garpix_catalog.models import ProductSku, Size, Color
    import random
    sizes = Size.objects.all()
    colors = Color.objects.all()
    try:
        skus = ProductSku.objects.all()
        for s in skus:
            if not s.size:
                size = random.choice(sizes)
                s.size = size
                s.save()
                print(s, 'size fixed')
            if not s.color:
                color = random.choice(colors)
                s.color = color
                s.save()
                print(s, 'color fixed')
    except Exception as e:
        print('fix_empty_colors_and_sizes() - error:', str(e))


'''
python backend/manage.py shell -c "from utils.some_scripts import update_cart_items; update_cart_items()"
'''
def update_cart_items():
    from garpix_cart_rest.models import Cart, CartItem
    try:
        cart_items = CartItem.objects.all()
        for ci in cart_items:
            ci.save()
        print('update_cart_items() - done')
    except Exception as e:
        print('update_cart_items() - error:', str(e))


'''
python backend/manage.py shell -c "from utils.some_scripts import fix_product_slugs; fix_product_slugs()"
'''
def fix_product_slugs():
    from garpix_catalog.models import Product
    try:
        products = Product.objects.all()
        for p in products:
            if '-none-' in p.slug:
                id_str = f'-{p.id}-'
                slug = p.slug.replace('-none-', id_str)
                p.slug = slug
                p.save()
        print('fix_product_slugs() - done')
    except Exception as e:
        print('fix_product_slugs() - error:', str(e))


'''
python backend/manage.py shell -c "from utils.some_scripts import create_shop_users; create_shop_users(5)"
'''
def create_shop_users(count=50):
    from user.models import User
    from shop.models import Shop
    try:
        for n in range(count):
            for shop in Shop.objects.all():
                user = User.objects.create(
                    username=f'some_user_{n+1}_shop_{shop.id}',
                    is_shop_buyer=True,
                    status=3,
                )
                user.set_password('jeka2017')
                user.save()
        print('create_shop_users() - done')
    except Exception as e:
        print('create_shop_users() - error:', str(e))
