'''
python backend/manage.py shell -c "from utils.delete_excess import delete_excess; delete_excess()"
'''
from user.models import AlreadySaw
from user.models import WishListItem


def delete_excess():
    print('---------')
    already_saw = AlreadySaw.objects.all()
    already_saw_excess_list = []
    for item in already_saw:
        if AlreadySaw.objects.filter(profile=item.profile, product=item.product).count() > 1:
            item.delete()
    print('---------')
    wishlist = WishListItem.objects.all()
    wishlist_excess_list = []
    for item in wishlist:
        if WishListItem.objects.filter(profile=item.profile, product=item.product).count() > 1:
            item.delete()
    print('---------')
