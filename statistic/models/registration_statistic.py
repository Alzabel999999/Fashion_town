from django.utils.timezone import now
from solo.models import SingletonModel
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook


class RegistrationStatistic(SingletonModel):

    class Meta:
        verbose_name = '01 - Статистика по количеству регистраций'

    @classmethod
    def generate_doc(cls, datetime_from, datetime_to, retailers_count, dropshippers_count, wholesaler_count):
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = 'Статистика регистрации'
        worksheet['A1'] = 'Дата от: '
        worksheet['A2'] = datetime_from
        worksheet['B1'] = 'Дата до: '
        worksheet['B2'] = datetime_to
        worksheet['C1'] = 'Роли:'
        worksheet['C2'] = 'Розница'
        worksheet['C3'] = 'Дропшипперов'
        worksheet['C4'] = 'Оптовиков'
        worksheet['C5'] = 'Итого: '
        worksheet['D1'] = 'Количество зарегистрированных пользователей'
        worksheet['D2'] = retailers_count
        worksheet['D3'] = dropshippers_count
        worksheet['D4'] = wholesaler_count
        worksheet['D5'] = (retailers_count + dropshippers_count + wholesaler_count)
        current_datetime = now()
        workbook.save(f'public/media/Статистика {current_datetime}.xlsx')
        current_datetime = str(current_datetime)
        current_datetime = current_datetime[0:16]

        response = HttpResponse(content=save_virtual_workbook(workbook))
        # mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        response['Content-Disposition'] = f'attachment; filename={current_datetime}.xlsx'
        return response
