from solo.models import SingletonModel


class ManagersOrdersStatistic(SingletonModel):

    class Meta:
        verbose_name = '05 - Статистика по каждому из менеджеров сколько единиц выкуплено/упаковано и совокупно'
