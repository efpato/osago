#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import logging
from datetime import timedelta

from pytractor.webdriver import Firefox

from osago.loader import load, monthdelta
from osago.ugsk.pages.login import LoginPage


logging.basicConfig(format=("%(asctime)s  %(levelname)-8s "
                            "%(module)-15s %(message)s"),
                    level=logging.DEBUG)
logging.getLogger(
    "selenium.webdriver.remote.remote_connection").setLevel(logging.WARNING)


def main():
    parser = argparse.ArgumentParser(prog="ugsk")
    parser.add_argument('email', help='User e-mail')
    parser.add_argument('password', help="User password")
    parser.add_argument('file', help='JSON-file with data')

    try:
        args = parser.parse_args()
        data = load(args.file)
    except Exception as e:
        parser.error(e)

    exit_code = 0
    try:
        driver = Firefox()
        driver.maximize_window()
        driver.set_script_timeout(60)
        driver.get('https://e-osago.ugsk.ru/osago/policy/')

        # Auth
        page = LoginPage(driver)
        page = page.login(args.email, args.password)

        # Insurer
        insurer = data['insurer']
        page.lastname = insurer['lastname']
        page.firstname = insurer['firstname']
        page.middlename = insurer['middlename']
        page.birthday = insurer['birthday'].strftime('%d.%m.%Y')
        page.doc_type.select_by_text(insurer['document']['type'])
        page.doc_series = insurer['document']['series']
        page.doc_number = insurer['document']['number']
        page.phone = '+7%s' % insurer['phone']
        page.registration_address = insurer['document']['address']
        page.confirm()
        page = page.next()

        # Owner
        page.wait_for_load()
        page.owner_is_insurer()
        owner = data['owner']
        page.lastname = owner['lastname']
        page.firstname = owner['firstname']
        page.middlename = owner['middlename']
        page.birthday = owner['birthday'].strftime('%d.%m.%Y')
        page.doc_type.select_by_text(owner['document']['type'])
        page.doc_series = owner['document']['series']
        page.doc_number = owner['document']['number']
        page.registration_address = owner['document']['address']
        page = page.next()

        # Vehicle
        vehicle = data['vehicle']
        if vehicle['purposeOfUse'] == 'Личные':
            page.purpose.select_by_text('Личная')
        elif vehicle['purposeOfUse'] == 'Учебная езда':
            page.purpose.select_by_text('Учебная езда')
        elif vehicle['purposeOfUse'] == 'Регулярные пассажирские перевозки':
            page.purpose.select_by_text(('Регулярные пассажирские перевозки / '
                                         'перевозки пассажиров по заказам'))
        elif vehicle['purposeOfUse'] == 'Такси':
            page.purpose.select_by_text('Такси')
        elif vehicle['purposeOfUse'] == 'Прокат краткосрочная аренда':
            page.purpose.select_by_text('Прокат / краткосрочная аренда')
        elif vehicle['purposeOfUse'] == 'Дорожные и специальные ТС':
            page.purpose.select_by_text('Дорожные и специальные ТС')
        elif vehicle['purposeOfUse'] == 'Экстренные и коммунальные службы':
            page.purpose.select_by_text('Экстренные и коммунальные службы')
        elif vehicle['purposeOfUse'] == ('Перевозка опасных и легко '
                                         'воспламеняющихся грузов'):
            page.purpose.select_by_text(('Перевозка опасных и легко '
                                         'воспламеняющихся грузов'))
        elif vehicle['purposeOfUse'] == 'Прочее':
            page.purpose.select_by_text('Прочее')
        if vehicle['with_trailer']:
            page.with_trailer()
        page.mark.select_by_text(vehicle['mark'])
        page.model.select_by_text(vehicle['model'])
        page.year = vehicle['year']
        page.mark = vehicle['mark']
        page.model = vehicle['model']
        page.year = vehicle['year']
        if page.category.enabled:
            if vehicle['type'] == 'Мотоциклы, мопеды и легкие квадрициклы':
                page.category.select_by_text('Мотоцикл (A)')
            elif vehicle['type'] == 'Мопеды, велосипеды':
                page.category.select_by_text('Мопед (М)')
            elif vehicle['type'] == 'Легковые автомобили':
                page.category.select_by_text('Легковое (B, BE)')
            elif vehicle['type'] == 'Грузовые автомобили':
                page.category.select_by_text('Грузовое (C, CE)')
            elif vehicle['type'] == 'Автобусы':
                page.category.select_by_text('Автобус (D, DE)')
            elif vehicle['type'] == 'Прицепы к грузовым автомобилям':
                page.category.select_by_text('Прицеп (E)')
            elif vehicle['type'] == 'Трамваи':
                page.category.select_by_text('Трамвай (Tm)')
            elif vehicle['type'] == 'Троллейбусы':
                page.category.select_by_text('Троллейбус (Tb)')
            elif vehicle['type'] == ('Тракторы, самоходные дорожно-'
                                     'строительные и иные машины, за '
                                     'исключением ТС, не имеющих колесных '
                                     'движ'):
                page.category.select_by_text('Трактор / Спецтехника')
        page.power = vehicle['power']
        page.power_kw = vehicle['powerKw']
        page.max_mass = vehicle['maxMass']
        page.seats_count = vehicle['seatsCount']
        if vehicle['registration']:
            page.registration()
        else:
            page.russia()
        if vehicle['document']['type'] == 'Паспорт ТС':
            page.doc_type.select_by_text('Паспорт ТС (ПТС)')
        elif vehicle['document']['type'] == 'Электронный ПТС':
            page.doc_type.select_by_text('Электронный ПТС (ЭПТС)')
        elif vehicle['document']['type'] == 'Свидетельство о регистрации ТС':
            page.doc_type.select_by_text('Свид-во о регистрации (СТС)')
        elif vehicle['document']['type'] == 'Техпаспорт':
            page.doc_type.select_by_text('Технический паспорт')
        page.doc_series = vehicle['document']['series']
        page.doc_number = vehicle['document']['number']
        page.doc_date_of_issue = vehicle['document']['dateOfIssue'].strftime(
            '%d.%m.%Y')
        page.reg_number = vehicle['regNumber']
        page.vin = vehicle['vin']
        page.inspection_card_number = vehicle['inspectionCard']['number']
        if vehicle['inspectionCard']['date'] is not None:
            page.inspection_card_date = vehicle['inspectionCard'][
                'date'].strftime('%d.%m.%Y')
        page = page.next()

        # Drivers
        page.multidrive(data['multidrive'])
        if not data['multidrive']:
            for i, dvr in enumerate(data['drivers']):
                if i > 0:
                    page.add_driver.click()
                page.lastname = dvr['lastname']
                page.firstname = dvr['firstname']
                page.middlename = dvr['middlename']
                page.birthday = dvr['birthday'].strftime('%d.%m.%Y')
                page.doc_series = dvr['license']['series']
                page.doc_number = dvr['license']['number']
                page.experience_from = dvr['experienceFrom'].strftime(
                    '%d.%m.%Y')
        page = page.next()

        # Terms
        page.policy_date_start = data['terms']['start'].strftime('%d.%m.%Y')
        page.policy_date_end = data['terms']['end'].strftime('%d.%m.%Y')
        page.period = monthdelta(data['periods'][0]['start'],
                                 data['periods'][0]['end'] + timedelta(days=1))
        page.period_start = data['periods'][0]['start'].strftime('%d.%m.%Y')
        page.period_end = data['periods'][0]['end'].strftime('%d.%m.%Y')
        page = page.next()

        # Extra
        page.delivery_electronically()
        page = page.next()

        # Payment
        page.wait_for_rsa_check()
        page.confirm()
        page.redirect.click()
        page.wait_for_rsa_check()

        print(page.webdriver.current_url)
    except Exception as e:
        logging.exception(e)
        exit_code = 1
    finally:
        driver.quit()

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
