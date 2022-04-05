from django.http import HttpResponse
from django.utils.timezone import now
from solo.models import SingletonModel
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook


class OrdersPerCityStatistic(SingletonModel):

    class Meta:
        verbose_name = '10 - Статистика по городам'

    @classmethod
    def generate_doc(cls, citys, counts):
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = 'Статистика по количеству заказов из городов'
        worksheet['A1'] = 'Города: '
        i = 2
        for city in citys:
            worksheet[f'A{i}'] = city
            i += 1
        worksheet['B1'] = 'Кол-во заказов: '
        i = 2
        for count in counts:
            worksheet[f'B{i}'] = count
            i += 1
        current_datetime = now()
        workbook.save(f'public/media/Статистика {current_datetime}.xlsx')
        current_datetime = str(current_datetime)
        current_datetime = current_datetime[0:16]

        response = HttpResponse(content=save_virtual_workbook(workbook))
        # mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        response['Content-Disposition'] = f'attachment; filename={current_datetime}.xlsx'
        return response
