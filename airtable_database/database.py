import pprint

from airtable import Airtable


class AirtableTable:
    def __init__(self, base_key, table_name, api_key):
        self.airtable = Airtable(base_key, table_name, api_key)

    def get_all_records(self):
        return self.airtable.get_all()

    def get_records(self, formula):
        return self.airtable.get_all(formula=formula)

    def get_record(self, record_id):
        return self.airtable.get(record_id)

    def create_record(self, fields):
        return self.airtable.insert(fields)

    def update_record(self, record_id, fields):
        return self.airtable.update(record_id, fields)


class Client:
    def __init__(self, base_key, api_key):
        self.table = AirtableTable(base_key, 'Клиенты', api_key)

    def get_all_clients(self):
        return self.table.get_all_records()

    def get_client_by_id_user(self, id_user):
        formula = f"{{ID}} = '{id_user}'"
        return self.table.get_records(formula)

    def create_client(self, id_user, phone, name, surname, mail):
        fields = {'ID': id_user,'Номер телефона': phone, 'Имя': name, 'Фамилия': surname, 'Почта': mail}
        return self.table.create_record(fields)

    def update_client(self, client_id, phone=None, name=None, surname=None, mail=None):
        fields = {}
        if phone:
            fields['Номер телефона'] = phone
        if name:
            fields['Имя'] = name
        if surname:
            fields['Фамилия'] = surname
        if mail:
            fields['Почта'] = mail
        return self.table.update_record(client_id, fields)


class Sport:
    def __init__(self, base_key, api_key):
        self.table = AirtableTable(base_key, 'Спорт', api_key)

    def get_all_sports(self):
        return self.table.get_all_records()

    def get_all_sports_unique(self):
        all_records = self.table.get_all_records()

        unique_sports = {}

        for record in all_records:
            sport_type = record['fields']['Тип спорта']

            if sport_type not in unique_sports:
                unique_sports[sport_type] = record

            else:
                existing_record = unique_sports[sport_type]
                if record['id'] != existing_record['id']:
                    unique_sports[sport_type] = record

        return list(unique_sports.values())

    def get_sport_by_type(self, sport_type):
        formula = f"{{Тип спорта}} = '{sport_type}'"
        return self.table.get_records(formula)

    def create_sport(self, sport_type, description, date_starting):
        fields = {'Тип спорта': sport_type, 'Описание': description, 'Дата проведения': date_starting}
        return self.table.create_record(fields)

    def update_sport(self, sport_id, sport_type=None, description=None, date_starting=None):
        fields = {}
        if sport_type:
            fields['Тип спорта'] = sport_type
        if description:
            fields['Описание'] = description
        if date_starting:
            fields['Дата проведения'] = date_starting
        return self.table.update_record(sport_id, fields)


class Record:
    def __init__(self, base_key, api_key):
        self.table = AirtableTable(base_key, 'Заявки', api_key)

    def get_all_records(self):
        return self.table.get_all_records()

    def get_records_by_client_id(self, id_user):
        formula = f"{{ID}} = '{id_user}'"
        return self.table.get_records(formula)

    def get_records_by_sport_type(self, sport_type):
        formula = f"{{Тип спорта}} = '{sport_type}'"
        return self.table.get_records(formula)

    def create_record(self, sport_type, id_user):
        fields = {'Тип спорта': sport_type, 'ID': id_user}
        return self.table.create_record(fields)


