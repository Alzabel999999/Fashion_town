from django.http import HttpResponse
from django.utils.timezone import now
from solo.models import SingletonModel
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook


class RevenueSumStatistic(SingletonModel):

    class Meta:
        verbose_name = '11 - Статистика по сумме выручки'

    @classmethod
    def generate_doc(cls, datetime_from, datetime_to, orders_count, price_sum, purchase_price_sum, revenue):
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = 'Статистика выручки (разница себестоимости и цен продаж за выбранный период)'
        worksheet['A1'] = 'Дата от: '
        worksheet['A2'] = datetime_from
        worksheet['B1'] = 'Дата до: '
        worksheet['B2'] = datetime_to
        worksheet['C1'] = 'Всего заказов:'
        worksheet['C2'] = orders_count
        worksheet['D1'] = 'Заказы на сумму:'
        worksheet['D2'] = price_sum
        worksheet['E1'] = 'Их себестоимость: '
        worksheet['E2'] = purchase_price_sum
        worksheet['F1'] = 'Выручка:'
        worksheet['F2'] = revenue
        current_datetime = now()
        workbook.save(f'public/media/Статистика {current_datetime}.xlsx')
        current_datetime = str(current_datetime)
        current_datetime = current_datetime[0:16]

        response = HttpResponse(content=save_virtual_workbook(workbook))
        # mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        response['Content-Disposition'] = f'attachment; filename={current_datetime}.xlsx'
        return response
