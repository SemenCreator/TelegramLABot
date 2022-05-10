from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


start_button = KeyboardButton('Продолжить')

start_kb = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True)

start_kb.add(start_button)

female_gender = KeyboardButton('Женский')
male_gender = KeyboardButton('Мужской')

choose_gender = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True)

choose_gender.add(female_gender, male_gender)

favourite_subjects = ReplyKeyboardMarkup(resize_keyboard=True)

subjects = 'Я люблю все предметы; русский язык; литература; алгебра; геометрия; \
иностранный язык; история; физическая культура; музыка; технология; химия; \
биология; физика; экология; ИЗО; информатика и ИКТ; география; естествознание;\
 астрономия; обществознание; ОБЖ; экономика; \
Мне не нравятся все предметы'.split("; ")


for subject in subjects:
    if subject != subjects[1] and subject != subjects[-1]:
        favourite_subjects.insert(KeyboardButton(subject))
    else:
        favourite_subjects.add(KeyboardButton(subject))


start_search_kb = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True)

choose_search_1 = KeyboardButton('Меня все устраивает')
choose_search_2 = KeyboardButton('Заполнить анкету заново')

start_search_kb.add(choose_search_1, choose_search_2)


edit_form_kb = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True)

repeat_form = KeyboardButton('Заполнить анкету заново')
edit_photo_form = KeyboardButton('Редактировать фото')
edit_description_form = KeyboardButton('Редактировать описание')
edit_subjects_form = KeyboardButton('Выбрать любимые предметы')
main_menu = KeyboardButton('Главное меню')

edit_form_kb.add(repeat_form).add(edit_photo_form, edit_description_form
                                  ).add(edit_subjects_form).add(main_menu)

main_kb = ReplyKeyboardMarkup(resize_keyboard=True)

watch_forms = KeyboardButton('Смотреть анкеты')
sympathy = KeyboardButton('Симпатия')
edit_form = KeyboardButton('Редактировать анкету')
edit_search = KeyboardButton('Редактировать поиск')

main_kb.add(watch_forms).add(sympathy).add(edit_form).add(edit_search)
