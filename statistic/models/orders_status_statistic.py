from django.http import HttpResponse
from django.utils.timezone import now
from solo.models import SingletonModel
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook


class OrdersStatusStatistic(SingletonModel):

    class Meta:
        verbose_name = '04 - Статистика по количеству выкупленных товаров, завершенных заявок, замен'

    @classmethod
    def generate_doc(cls, datetime_from, datetime_to,
                     items_redeemed, items_replacement,
                     orders_closed, orders_percent,
                     items_redeemed_percent, items_replacement_percent):
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = 'Статистика выкупленных товаров, завершенных заявок, замен и их процентное соотношение.'
        worksheet['A1'] = 'Дата от: '
        worksheet['A2'] = datetime_from
        worksheet['B1'] = 'Дата до: '
        worksheet['B2'] = datetime_to
        worksheet['C1'] = 'Кол-во выкупленных товаров:'
        worksheet['C2'] = items_redeemed
        worksheet['D1'] = 'Завершенных заявок:'
        worksheet['D2'] = orders_closed
        worksheet['E1'] = 'Кол-во замен:'
        worksheet['E2'] = items_replacement
        worksheet['F1'] = "Процентное соотношение(Все / Выкупленные):"
        worksheet['F2'] = orders_percent
        worksheet['G1'] = "Процентное соотношение(Все / Завершенные):"
        worksheet['G2'] = items_redeemed_percent
        worksheet['H1'] = "Процентное соотношение(Все / Замены):"
        worksheet['H2'] = items_replacement_percent
        current_datetime = now()
        workbook.save(f'public/media/Статистика {current_datetime}.xlsx')
        current_datetime = str(current_datetime)
        current_datetime = current_datetime[0:16]

        response = HttpResponse(content=save_virtual_workbook(workbook))
        # mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        response['Content-Disposition'] = f'attachment; filename={current_datetime}.xlsx'
        return response
