from django.db import models


class Currency(models.Model):

    class CURENCY_NAME:
        RUB = 'RUB'
        BYN = 'BYN'
        UAH = 'UAH'
        KZT = 'KZT'
        USD = 'USD'
        EUR = 'EUR'
        TYPES = (
            (RUB, 'Российский рубль'),
            (BYN, 'Белорусский рубль'),
            (UAH, 'Украинская гривна'),
            (KZT, 'Казахстанский тенге'),
            (USD, 'Американский доллар'),
            (EUR, 'Евро'),
        )

    title = models.CharField(
        max_length=3, unique=True, verbose_name='Валюта', choices=CURENCY_NAME.TYPES, default=CURENCY_NAME.RUB)
    ratio = models.DecimalField(max_digits=8, decimal_places=4, default=0.0000, verbose_name='Курс')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'

    @classmethod
    def get_currencies_from_bank(cls):
        '''
        python backend/manage.py shell -c "from garpix_catalog.models.currency import Currency; Currency.get_currencies_from_bank(Currency)"
        '''
        import requests
        from bs4 import BeautifulSoup

        response = requests.get('https://www.nbp.pl/kursy/xml/dir.txt', )
        tab_list = response.content.decode('utf-8').split('\r\n')
        a_tab_list = []
        for t in tab_list:
            if t.startswith('a'):
                a_tab_list.append(t)
        last_tab = a_tab_list[-1]

        url = 'https://www.nbp.pl/kursy/xml/%s.xml' % (last_tab)
        response = requests.get(url)

        currency_tabl = BeautifulSoup(response.content.decode('latin'), features='lxml')
        kod_waluty_list = currency_tabl.findAll('kod_waluty')
        for kod_waluty in kod_waluty_list:
            if kod_waluty.contents[0] == 'RUB':
                obj = Currency.objects.get(title=kod_waluty.contents[0])
                obj.update_currency(float(kod_waluty.parent.find('kurs_sredni').contents[0].replace(',', '.')))
            if kod_waluty.contents[0] == 'BYN':
                obj = Currency.objects.get(title=kod_waluty.contents[0])
                obj.update_currency(float(kod_waluty.parent.find('kurs_sredni').contents[0].replace(',', '.')))
            if kod_waluty.contents[0] == 'UAH':
                obj = Currency.objects.get(title=kod_waluty.contents[0])
                obj.update_currency(float(kod_waluty.parent.find('kurs_sredni').contents[0].replace(',', '.')))
            if kod_waluty.contents[0] == 'KZT':
                obj = Currency.objects.get(title=kod_waluty.contents[0])
                obj.update_currency(float(kod_waluty.parent.find('kurs_sredni').contents[0].replace(',', '.')))
            if kod_waluty.contents[0] == 'USD':
                obj = Currency.objects.get(title=kod_waluty.contents[0])
                obj.update_currency(float(kod_waluty.parent.find('kurs_sredni').contents[0].replace(',', '.')))
            if kod_waluty.contents[0] == 'EUR':
                obj = Currency.objects.get(title=kod_waluty.contents[0])
                obj.update_currency(float(kod_waluty.parent.find('kurs_sredni').contents[0].replace(',', '.')))

    def update_currency(self, ratio):
        self.ratio = ratio
        self.save()
