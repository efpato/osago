# -*- coding: utf-8 -*-

import calendar
import datetime
import json


def load(filename):
    with open(filename) as fp:
        data = json.load(fp)

    data = data['data']['entity']

    return {
        'insurer': {
            'lastname': data['Strahovatel']['NaFa'],
            'firstname': data['Strahovatel']['Imya'],
            'middlename': data['Strahovatel']['Otchestvo'],
            'birthday': datetime.datetime.strptime(
                data['Strahovatel']['DataRozhdeniya'], '%Y-%m-%dT%H:%M:%S'),
            'document': {
                'type': data['UdostoverenieStrahovatelya']['Vid'][
                    'NaimObekta'].split(' ', 1)[1],
                'series': data['UdostoverenieStrahovatelya']['Seriya'],
                'number': data['UdostoverenieStrahovatelya']['Nomer'],
                'dateOfIssue': datetime.datetime.strptime(
                    data['UdostoverenieStrahovatelya']['Data'],
                    '%Y-%m-%dT%H:%M:%S'),
                'organizationOfIssue': data['UdostoverenieStrahovatelya'][
                    'Vydan'],
                'address': data['AdresStrahovatelya']['Adres']
            },
            'phone': sorted(
                ((o['IDObekta'], o['Znachenie'])
                 for o in data['Strahovatel']['Kontakty']
                 if o['VidKontaktov']['Naim'] == 'Телефон мобильный'),
                key=lambda t: t[0])[-1][1]
        },
        'owner': {
            'lastname': data['ObektStrahPoDog'][0]['ObektStrah']['Vladelec'][
                'NaFa'],
            'firstname': data['ObektStrahPoDog'][0]['ObektStrah']['Vladelec'][
                'Imya'],
            'middlename': data['ObektStrahPoDog'][0]['ObektStrah']['Vladelec'][
                'Otchestvo'],
            'birthday': datetime.datetime.strptime(
                data['ObektStrahPoDog'][0]['ObektStrah']['Vladelec'][
                    'DataRozhdeniya'], '%Y-%m-%dT%H:%M:%S'),
            'document': {
                'type': data['ObektStrahPoDog'][0]['ObektStrah'][
                    'UdostovSobstvennika']['Vid'][
                        'NaimObekta'].split(' ', 1)[1],
                'series': data['ObektStrahPoDog'][0]['ObektStrah'][
                    'UdostovSobstvennika']['Seriya'],
                'number': data['ObektStrahPoDog'][0]['ObektStrah'][
                    'UdostovSobstvennika']['Nomer'],
                'dateOfIssue': datetime.datetime.strptime(
                    data['ObektStrahPoDog'][0]['ObektStrah'][
                        'UdostovSobstvennika']['Data'], '%Y-%m-%dT%H:%M:%S'),
                'organizationOfIssue': data['ObektStrahPoDog'][0][
                    'ObektStrah']['UdostovSobstvennika']['Vydan'],
                'address': data['ObektStrahPoDog'][0]['ObektStrah'][
                    'AdresSobstvennika']['Adres']
            },
            'phone': sorted(
                ((o['IDObekta'], o['Znachenie'])
                 for o in data['ObektStrahPoDog'][0]['ObektStrah']['Vladelec'][
                     'Kontakty']
                 if o['VidKontaktov']['Naim'] == 'Телефон мобильный'),
                key=lambda t: t[0])[-1][1]
        },
        'vehicle': {
            'type': data['ObektStrahPoDog'][0]['ObektStrah']['TipTS'][
                'NaimObekta'],
            'mark': data['ObektStrahPoDog'][0]['ObektStrah']['MarkaPTS'],
            'model': data['ObektStrahPoDog'][0]['ObektStrah']['ModelPTS'],
            'vin': data['ObektStrahPoDog'][0]['ObektStrah']['VIN'],
            'year': data['ObektStrahPoDog'][0]['ObektStrah']['GodPostrojki'],
            'power': data['ObektStrahPoDog'][0]['ObektStrah']['Moshhnost'],
            'powerKw': data['ObektStrahPoDog'][0]['ObektStrah'][
                'MoshhnostVt'],
            'maxMass': data['ObektStrahPoDog'][0]['ObektStrah']['MaksMassa'],
            'seatsCount': data['ObektStrahPoDog'][0]['ObektStrah'][
                'ChisloMest'],
            'registration': data['ObektStrahPoDog'][0]['ObektStrah'][
                'SledovanieKMestuRegistracii'],
            'document': {
                'type': data['ObektStrahPoDog'][0]['ObektStrah']['VidDokTS'][
                    'NaimObekta'],
                'series': data['ObektStrahPoDog'][0]['ObektStrah'][
                    'SeriyaSvidetOReg'],
                'number': data['ObektStrahPoDog'][0]['ObektStrah'][
                    'NomerSvidetOReg'],
                'dateOfIssue': datetime.datetime.strptime(
                    data['ObektStrahPoDog'][0]['ObektStrah']['DataSvidetOReg'],
                    '%Y-%m-%dT%H:%M:%S')
            },
            'inspectionCard': {
                'number': data['ObektStrahPoDog'][0]['ObektStrah']['DokPoTS'][
                    'Nomer'],
                'date': (datetime.datetime.strptime(
                    data['ObektStrahPoDog'][0]['ObektStrah']['DokPoTS'][
                        'DataSledTO'], '%Y-%m-%dT%H:%M:%S')
                         if data['ObektStrahPoDog'][0]['ObektStrah'][
                             'DokPoTS']['DataSledTO'] is not None
                         else None)
            },
            'purposeOfUse': data['ObektStrahPoDog'][0]['ObektStrah'][
                'CelIspolzovaniyaTS']['NaimObekta'].split(' ', 1)[1],
            'regNumber': data['ObektStrahPoDog'][0]['ObektStrah'][
                'RegistrZnak'],
            'with_trailer': data['PriznakStrahPricep']
        },
        'multidrive': data['DopuskKUpravDlyaVsehTS'],
        'drivers': [
            {
                'lastname': driver['Voditel']['FL']['NaFa'],
                'firstname': driver['Voditel']['FL']['Imya'],
                'middlename': driver['Voditel']['FL']['Otchestvo'],
                'birthday': datetime.datetime.strptime(
                    driver['Voditel']['FL']['DataRozhdeniya'],
                    '%Y-%m-%dT%H:%M:%S'),
                'license': {
                    'series': driver['Voditel']['Prava']['Seriya'],
                    'number': driver['Voditel']['Prava']['Nomer'],
                    'dateOfIssue': datetime.datetime.strptime(
                        driver['Voditel']['Prava']['Data'],
                        '%Y-%m-%dT%H:%M:%S')
                },
                'experienceFrom': datetime.datetime.strptime(
                    driver['Voditel']['DataNachalaStazha'],
                    '%Y-%m-%dT%H:%M:%S')
            }
            for driver in data['VoditeliDogStrah']
        ],
        'terms': {
            'start': datetime.datetime.strptime(
                data['DataNachalaDejstviya'], '%Y-%m-%dT%H:%M:%S'),
            'end': datetime.datetime.strptime(
                data['DataOkonchaniyaDejstviya'], '%Y-%m-%dT%H:%M:%S')
        },
        'periods': [
            {
                'start': (datetime.datetime.strptime(data['PINachalo1'],
                                                     '%Y-%m-%dT%H:%M:%S')
                          if data['PINachalo1'] is not None else None),
                'end': (datetime.datetime.strptime(data['PIOkonchanie1'],
                                                   '%Y-%m-%dT%H:%M:%S')
                        if data['PINachalo1'] is not None else None),
            },
            {
                'start': (datetime.datetime.strptime(data['PINachalo2'],
                                                     '%Y-%m-%dT%H:%M:%S')
                          if data['PINachalo2'] is not None else None),
                'end': (datetime.datetime.strptime(data['PIOkonchanie2'],
                                                   '%Y-%m-%dT%H:%M:%S')
                        if data['PINachalo2'] is not None else None),
            },
            {
                'start': (datetime.datetime.strptime(data['PINachalo3'],
                                                     '%Y-%m-%dT%H:%M:%S')
                          if data['PINachalo3'] is not None else None),
                'end': (datetime.datetime.strptime(data['PIOkonchanie3'],
                                                   '%Y-%m-%dT%H:%M:%S')
                        if data['PINachalo3'] is not None else None),
            }
        ]
    }


def monthdelta(d1, d2):
    delta = 0
    while True:
        mdays = calendar.monthrange(d1.year, d1.month)[1]
        d1 += datetime.timedelta(days=mdays)
        if d1 <= d2:
            delta += 1
        else:
            break
    return delta
