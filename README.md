# Финальный экзаменационный проеткт для [SkillFactory](https://skillfactory.ru)
###### Студент: Гончаров Юрий

## Список тестов:

Было создано 53 автотеста для сайта [E-katalog](https://www.e-katalog.ru)
1. Проверка регистрации
    - [ ] Через Google
    - [ ] Через Facebook
    - [ ] Через ВКонтакте
    - [X] С помощью своего email
2. Проверка страницы пользователя
    - [X] От лица этого пользователя
    - [X] От лица другого пользователя
    - [X] Проверка изменения информации
        - [X] С правильным вводом пароля
        - [X] С неправильным вводом пароля
        - [X] С js-скриптом
3. Проверка страницы поиска товаров
    - [X] Все вкладки с товарами работают
    - [X] Вкладки с популярными производителями показывают товары только этих производителей
    - [X] Фильтр по цене работает верно
    - [X] Фильтр по производителям работает верно
    - [X] Фильтр по остальным приколюхам работает верно
4. Остальное
    - [ ] Проверка добавления товара в закладки
    - [ ] Проверка сравнивания товаров

## Описание тестов:

1. tests_on_main_page.py
    1. test_access_to_main_page
        - Проверка, что страница загружается
    2. test_register_user_good_input
        - Проверка регистрации пользователя с верным вводом
    3. test_register_user_bad_input
        - Проверка регистрации пользователя с неверными данными
2. tests_on_profile_page.py
   1. test_access_to_my_profile
      - Проверка, что страница загружается
   2. test_my_profile_without_cookie
      - Проверка моей страницы от лица другого пользователя
   3. test_edit_profile
      - Проверка изменения информации о пользователе
3. tests_on_search_page.py
   1. test_access_to_search_page
      - Проверка, что страница загружается
   2. test_title_of_products
      - Проверка кнопок популярных производилелей
   3. test_filter_products
      - Проверка фильтра товаров

## Запуск тестов

Я запускал через браузер `Chrome` (он приложен в репозитории) с помощью команды:
```
   python3 -m pytest --driver Chrome --driver-path ./chromedriver tests/*
```
Для Windows, скорее всего, нужно указать другой пусть к бинарнику браузера