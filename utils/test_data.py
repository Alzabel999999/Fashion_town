brand_list = {'MeGu': 2, 'ByMe': 2, 'Caramella': 2, 'Luisa': 2, 'Betta️': 2, 'Mylala': 2,
              'La Blanche': 2, 'Minouu': 2, 'My Vogue': 2, 'MiMi (KiWi)': 5, 'Ingrosso': 9, 'Cocomore': 9,
              'Paparazzi Fashion': 2, 'Prestigio Fashion': 2, 'Bastet': 10, 'Madnes': 2, 'MaGnes': 2,
              'By O La La': 2, 'Lamur': 3, 'LaLeLi': 2, 'Pilsiti': 2, 'Lenoshka': 2, 'Manuel': 1,
              'Piękne': 0, 'ТМС': 0, 'Lollite': 2, 'Bianka': 3, 'Made in Poland': 3, 'Madam Sue': 2,
              'Mood': 2, 'By Love': 2, 'Corso': 1, 'Сосо': 2, 'Pretty Women': 2, 'S. Moriss': 1,
              'Miss Fofo': 2, 'Varleska': 1, 'Meluve': 1, 'Biertex': 2, 'Motion': 6, 'Infinite': 1,
              'Bocca': 2, 'Migalo': 3, 'BLV': 2, 'Edan': 2, 'La Moni': 2, 'Malina': 3, 'Gianmarko': 0}

categories = {
    'Футболки': {'parent': '', 'product_list': ['Футболка', 'Майка']},
    'Толстовки': {'parent': '', 'product_list': ['Толстовка', 'Худи']},
    'Брюки': {'parent': '', 'product_list': ['Штаны', 'Брюки']},
    'Джинсы': {'parent': '', 'product_list': ['Джинсы', 'Джинсы']},
    'Свитера и кардиганы': {'parent': '', 'product_list': ['Свитер', 'Кардиган']},
    'Верхняя одежда': {'parent': '', 'product_list': ['Куртка джинсовая', 'Куртка длинная']},
    'Шубы': {'parent': 'Верхняя одежда', 'product_list': ['шуба норковая', 'Шуба песцовая']},
    'Куртки': {'parent': 'Верхняя одежда', 'product_list': ['Куртка балоневая', 'Куртка летняя']},
    'Пальто': {'parent': 'Верхняя одежда', 'product_list': ['Пальто длинное', 'Пальто короткое']},
    'Плащи': {'parent': 'Верхняя одежда', 'product_list': ['Плащ кожаный', 'Плащ']},
    'Альпаки': {'parent': 'Верхняя одежда', 'product_list': ['Альпак военный', 'Альпак арктический']},
    'Платья': {'parent': '', 'product_list': ['Платье-пачка', 'Платье-майка']},
    'Миди': {'parent': 'Платья', 'product_list': ['Миди', 'Миди-юбка']},
    'Мини': {'parent': 'Платья', 'product_list': ['Мини-юбка', 'Мини-юбка']},
    'Макси': {'parent': 'Платья', 'product_list': ['Макси', 'Макси-юбка']},
    'Жилетки': {'parent': '', 'product_list': ['Жилетка летняя', 'Жилетка пуховая']},
    'Блузки/рубашки': {'parent': '', 'product_list': ['Блузка', 'Рубашка']},
    'Юбки': {'parent': '', 'product_list': ['Юбка длинная', 'Юбка короткая']},
    'Шорты': {'parent': '', 'product_list': ['Шорты', 'Шорты-мини']},
    'Пиджаки': {'parent': '', 'product_list': ['Пиджак женский', 'Пиджак офисный']},
    'Наборы/комплекты': {'parent': '', 'product_list': ['Костюм выходной', 'Костюм офисный']},
    'Аксессуары': {'parent': '', 'product_list': ['Цепочка', 'Зонт']},
    'Сумки': {'parent': 'Аксессуары', 'product_list': ['Сумка кожаная', 'Сумка']},
    'Шапки': {'parent': 'Аксессуары', 'product_list': ['Шапка песцовая', 'Шапкая пуховая']},
    'Шарфы': {'parent': 'Аксессуары', 'product_list': ['Шарф вязаный', 'Шарф плетеный']},
    'Перчатки': {'parent': 'Аксессуары', 'product_list': ['Перчатки флисовые', 'Перчатки кожаные']},
    'Комбезы': {'parent': '', 'product_list': ['Комбез рабочий', 'Комбез зимний']},
    'Обувь': {'parent': '', 'product_list': ['Кросовки', 'Сапоги', 'Балетки']},
    'Парфюм': {'parent': '', 'product_list': ['Парфюм', 'Духи']},
}

colors_list = {'Yellow': '#E9F314',
               'Red': '#FA0202',
               'Green': '#289E02',
               'Blue': '#02099E',
               'Pink': '#EA08C8',
               'White': '#FFFFFF',
               'Black': '#000000'}

users_list = [
    {'login': 'Dmitry', 'first_name': 'Дмитрий', 'last_name': 'Иванов',
     'e-mail': 'Dmitryivanov@gmail.com', 'password': '1234567890', 'role': 1},
    {'login': 'Vasiliy', 'first_name': 'Василий', 'last_name': 'Иванов',
     'e-mail': 'Vasiliyivanov@gmail.com', 'password': '1234567890', 'role': 1},
    {'login': 'Alina', 'first_name': 'Алина', 'last_name': 'Иванова',
     'e-mail': 'Alinaivanov@gmail.com', 'password': '1234567890', 'role': 2},
    {'login': 'Olga', 'first_name': 'Ольга', 'last_name': 'Иванова',
     'e-mail': 'Olgaivanov@gmail.com', 'password': '1234567890', 'role': 2},
    {'login': 'Mariya', 'first_name': 'Мария', 'last_name': 'Иванова',
     'e-mail': 'Mariyaivanov@gmail.com', 'password': '1234567890', 'role': 3},
    {'login': 'Ivan', 'first_name': 'Иван', 'last_name': 'Иванов',
     'e-mail': 'Ivanivanov@gmail.com', 'password': '1234567890', 'role': 3},
]

delivery_method_list = ['Почта Польши', 'СДЭК Польши', 'Почта России', 'СДЭК России', 'КАРГО']
payment_methods_list = ['Онлайн', 'Наличные', ]
