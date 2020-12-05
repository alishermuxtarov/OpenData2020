from re import compile, IGNORECASE
from traceback import print_exc
from json import loads
from math import ceil

from django.core.management import base

from weblib import error
from grab import Grab

from reference.models import Region, Area
from vehicle import models


class Skip(Exception):
    pass


REGIONS = {
    6: [216, 204, 94, 95, 96, 206, 210, 208, 212, 202, 98, 214, 100, 99, 103, 101, 102],
    27: [105, 104, 108, 107, 109, 110, 111, 220, 112, 113, 106, 218],
    28: [224, 238, 117, 118, 114, 115, 116, 222, 119, 120, 228, 226, 236, 230, 234, 232],
    32: [250, 122, 123, 130, 248, 244, 246, 124, 125, 126, 121, 131, 127, 252, 128, 129],
    29: [133, 144, 135, 134, 136, 240, 132, 137, 138, 139, 141, 242, 145, 143, 146, 140, 142],
    30: [258, 256, 254, 149, 147, 150, 260, 151, 152, 148],
    31: [158, 266, 159, 262, 154, 153, 155, 264, 156, 157, 160],
    33: [162, 163, 171, 274, 164, 165, 278, 280, 167, 168, 272, 268, 169, 276, 270, 161, 282, 170, 166],
    34: [284, 173, 288, 174, 175, 286, 176, 177, 178, 294, 290, 179, 180, 181, 172, 296, 298, 292],
    35: [183, 302, 310, 182, 304, 308, 300, 185, 184, 306, 312, 186, 314],
    5: [
        73, 74, 75, 76, 77, 316, 78, 322, 89, 90, 340, 324, 81, 91, 79, 80, 318, 336, 83, 84, 328, 85, 344, 330,
        88, 86, 87, 338, 4, 342, 332, 334, 320, 346, 92, 93, 82, 326
    ],
    36: [348, 350, 188, 354, 187, 189, 190, 191, 356, 192, 368, 358, 193, 370, 360, 362, 366, 194, 364, 374, 352, 372],
    37: [196, 380, 197, 378, 376, 198, 384, 195, 199, 382, 200, 386]
}


class Command(base.BaseCommand):
    # todo: вычислять кол-во страниц, и после в цикле проходить по всем
    UA = str(
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 '
        '(KHTML, like Gecko) Version/14.0.1 Safari/605.1.15')
    HEADERS = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.olx.uz',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.olx.uz/transport/legkovye-avtomobili/',
        'User-Agent': UA,
    }
    URL = 'https://www.olx.uz/ajax/search/list/'
    URL_XPATH = '//*[@class="photo-cell"]/a'
    PRICE_XPATH = str('//*[@class="offer-titlebox__price"]/'
                      'div[@class="pricelabel"]/strong')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.g = Grab()

    def get_usd_nbu(self):
        self.req('https://nbu.uz/en/exchange-rates/json/')
        if not self.g.doc.body:
            return 10480
        data = loads(self.g.doc.body)
        res = [d['cb_price'] for d in data if d['code'] == 'USD']
        return ceil(res[0])

    def req(self, url, **kw):
        self.g.go(url, headers=self.HEADERS, user_agent=self.UA, **kw)

    @staticmethod
    def get_vehicle_cat(page=1, **kwargs):
        defaults = {
            # 'search[city_id]': 4,
            # 'search[region_id]': 5,
            # 'search[district_id]': 0,
            'search[filter_float_motor_mileage:from]': 5,
            'search[category_id]': 108,
            'search[private_business]': 'private',
            'page': page
        }
        if kwargs:
            defaults.update(kwargs)
        return defaults

    def handle(self, *args, **options):
        self.load_defaults()
        for region, areas in REGIONS.items():
            print('Region ID', region)
            # for area in areas:
            #     print('Area ID', area)
            for page in range(1, 26):
                print('Page', page)
                self.req(self.URL, post=self.get_vehicle_cat(
                    page, **{
                        'search[region_id]': region,
                        # 'search[city_id]': area,
                    }
                ))
                urls = self.g.doc.select(self.URL_XPATH)
                for url in urls:
                    try:
                        self.parse_url(url.attr('href').split('#')[0])
                    except Exception as ex:
                        print('[err]', ex.__str__())
                        print_exc()

    def load_defaults(self):
        self.brands = dict(models.Brand.objects.values_list('name', 'id'))
        self.models = dict(models.Model.objects.values_list('name', 'id'))
        self.types = dict(models.BodyType.objects.values_list('name', 'id'))
        self.colors = dict(models.BodyColor.objects.values_list('name', 'id'))
        self.fuels = dict(models.FuelType.objects.values_list('name', 'id'))
        self.conditions = {v: k for k, v in models.VehicleCondition.choices}
        self.transmissions = {v: k for k, v in models.TransmissionType.choices}
        self.options = dict(models.AdditionalOption.objects.values_list('name', 'id'))
        self.regions = dict(Region.objects.values_list('name', 'id'))
        self.areas = dict(Area.objects.values_list('name', 'id'))
        self.stops = '|'.join(models.StopWord.objects.values_list('name', flat=True))
        self.stop = self.stops and compile(self.stops, IGNORECASE)
        self.usd = self.get_usd_nbu()

    @staticmethod
    def get_def_id(var, name, model, **kwargs):
        if name in var:
            return var[name]
        obj = model.objects.create(name=name, **kwargs)
        var[name] = obj.pk
        return obj.pk

    def get_brand_id(self, name):
        return self.get_def_id(self.brands, name, models.Brand)

    def get_model_id(self, name, **kwargs):
        return self.get_def_id(self.models, name, models.Model, **kwargs)

    def get_type_id(self, name):
        return self.get_def_id(self.types, name, models.BodyType)

    def get_color_id(self, name):
        return self.get_def_id(self.colors, name, models.BodyColor)

    def get_fuel_id(self, name):
        return self.get_def_id(self.fuels, name, models.FuelType)

    def get_option_id(self, name):
        return self.get_def_id(self.options, name, models.AdditionalOption)

    def get_condition(self, name):
        if not name:
            return
        return self.conditions[name]

    def get_transmission(self, name):
        if not name:
            return
        return self.transmissions[name]

    def get_region_id(self, name):
        return self.get_def_id(self.regions, name, Region)

    def get_area_id(self, name, **kwargs):
        return self.get_def_id(self.areas, name, Area, **kwargs)

    @staticmethod
    def get_int(value):
        return ''.join([s for s in str(value).split() if s.isdigit()])

    def parse_url(self, url):
        if models.VehicleAd.objects.filter(url=url).count():
            print('[skip]', url)
            return
        self.req(url)
        try:
            address = self.g.doc.select('//address').text().strip().split(',')
        except error.DataNotFound:
            print('[err addr]', url)
            return

        price = self.g.doc.select(self.PRICE_XPATH).text()
        title = self.g.doc.select('//h1').text().strip()
        description = self.g.doc.select('//div[@id="textContent"]').text().strip()
        if self.stops and (self.stop.search(title) or self.stop.search(description)):
            print('[ignore]', url)
            return

        print('+', url)

        if 'у.е.' in price:
            price_usd = price.replace('у.е.', '').replace(' ', '').split('.')[0]
            price_uzs = int(price_usd) * self.usd
        else:
            price_uzs = price.replace('сум', '').replace(' ', '').split('.')[0]
            if price_uzs == 'Обмен':
                return
            price_usd = ceil(int(price_uzs) / self.usd)

        brand_id = self.get_brand_id(self.attr("Марка"))
        model_id = self.get_model_id(self.attr("Модель"), brand_id=brand_id)
        type_id = self.get_type_id(self.attr("Тип кузова"))
        color_id = self.get_color_id(self.attr("Цвет"))
        fuel_id = self.get_fuel_id(self.attr("Вид топлива"))
        # todo: 4+ - подумать над этим
        number_of_owners = (self.attr("Количество хозяев") or '1').replace('4+', '5')
        region_id = self.get_region_id(address[1].strip())
        area_id = self.get_area_id(address[0].strip(), region_id=region_id)

        vehicle = models.VehicleAd.objects.create(
            source=models.AdSource.OLX,
            title=title or "",
            description=description or "",
            url=url,
            manufactured_year=self.attr("Год выпуска", '0') or 0,
            number_of_owners=number_of_owners,
            transmission_type=self.get_transmission(self.attr("Коробка передач")),
            condition=self.get_condition(self.attr("Состояние машины")),
            engine_capacity=self.get_int(self.attr("Объем двигателя") or 0),
            driven_km=self.get_int(self.attr("Пробег") or 0),
            price_usd=price_usd,
            price_uzs=price_uzs,
            brand_id=brand_id,
            model_id=model_id,
            body_type_id=type_id,
            body_color_id=color_id,
            fuel_types_id=fuel_id,
            region_id=region_id,
            area_id=area_id,
        )
        for option_id in self.get_options():
            vehicle.additional_options.add(models.AdditionalOption.objects.get(pk=option_id))

    def get_options(self):
        try:
            options = self.g.doc.select(
                '//span[contains(text(), "Доп. опции")]/../strong/a')
            options_list = []
            for option in options:
                option = (option.text() or '').strip()
                options_list.append(self.get_option_id(option))
            return options_list
        except error.DataNotFound:
            return []

    def attr(self, attr, default=''):
        try:
            return (self.g.doc.select(
                '//span[contains(text(), "{}")]/../strong'.format(attr)
            ).text() or '').strip()
        except error.DataNotFound:
            return default
