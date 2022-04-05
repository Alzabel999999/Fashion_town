from django.http import HttpResponse
from django.utils.timezone import now
from solo.models import SingletonModel
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook


class OverageItemsInOrdersStatistic(SingletonModel):

    class Meta:
        verbose_name = '08 - Статистика по среднему количеству товаров в посылке (без опта)'

    @classmethod
    def generate_doc(cls, datetime_from, datetime_to, all_orders, all_items, overage):
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = 'Статистика среднего кол-ва товаров в посылке (без опта).'
        worksheet['A1'] = 'Дата от: '
        worksheet['A2'] = datetime_from
        worksheet['B1'] = 'Дата до: '
        worksheet['B2'] = datetime_to
        worksheet['C1'] = 'Всего посылок:'
        worksheet['C2'] = all_orders
        worksheet['D1'] = 'Всего вещей:'
        worksheet['D2'] = all_items
        worksheet['E1'] = 'Вещей в посылке, в среднем: '
        worksheet['E2'] = overage
        current_datetime = now()
        workbook.save(f'public/media/Статистика {current_datetime}.xlsx')
        current_datetime = str(current_datetime)
        current_datetime = current_datetime[0:16]

        response = HttpResponse(content=save_virtual_workbook(workbook))
        # mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        response['Content-Disposition'] = f'attachment; filename={current_datetime}.xlsx'
        return response
