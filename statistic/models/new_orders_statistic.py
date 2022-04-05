from django.http import HttpResponse
from solo.models import SingletonModel
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
from django.utils.timezone import now


class NewOrdersStatistic(SingletonModel):

    class Meta:
        verbose_name = '02 - Статистика по количеству заказов новых пользователей'

    @classmethod
    def generate_doc(cls, datetime_from, datetime_to, wholesalers, dropshippers, retailers):
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = 'Статистика по количеству заказов новых пользователей'
        worksheet['A1'] = 'Дата от: '
        worksheet['A2'] = datetime_from
        worksheet['B1'] = 'Дата до:'
        worksheet['B2'] = datetime_to
        worksheet['C1'] = 'Оптовики'
        worksheet['C2'] = 'Никнеймы'
        worksheet['D2'] = 'Кол-во заказов'
        i = 3
        for users, counts in wholesalers:
            worksheet[f'C{i}'] = users
            worksheet[f'D{i}'] = counts
            i += 1
        worksheet['E1'] = 'Дропшиперы'
        worksheet['E2'] = 'Никнеймы'
        worksheet['F2'] = 'Кол-во заказов'
        i = 3
        for users, counts in dropshippers:
            worksheet[f'E{i}'] = users
            worksheet[f'F{i}'] = counts
            i += 1
        worksheet['G1'] = 'Розница'
        worksheet['G2'] = 'Никнеймы'
        worksheet['H2'] = 'Кол-во заказов'
        i = 3
        for users, counts in retailers:
            worksheet[f'G{i}'] = users
            worksheet[f'H{i}'] = counts
            i += 1
        current_datetime = now()
        workbook.save(f'public/media/Статистика {current_datetime}.xlsx')
        current_datetime = str(current_datetime)
        current_datetime = current_datetime[0:16]

        response = HttpResponse(content=save_virtual_workbook(workbook))
        # mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        response['Content-Disposition'] = f'attachment; filename={current_datetime}.xlsx'
        return response
