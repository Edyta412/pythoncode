import pickle
from collections import UserDict
from datetime import datetime

class AddressBook(UserDict):
    def __init__(self, page_size=5):
        super().__init__()
        self.page_size = page_size

    def find_records(self, search_term):
        results = []
        for record in self.values():
            if search_term.lower() in record.name.value.lower():
                results.append(record)
            for phone in record.phones:
                if search_term.lower() in phone.value:
                    results.append(record)
                    break
        return results

    def __iter__(self):
        self.page = 0
        self.current_page = self.paginate()
        return self

    def __next__(self):
        if self.page < len(self.current_page):
            record = self.current_page[self.page]
            self.page += 1
            return record
        else:
            raise StopIteration

    def paginate(self):
        return list(self.values())[self.page * self.page_size:(self.page + 1) * self.page_size]

    def save_to_disk(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.data, f)

    @classmethod
    def load_from_disk(cls, filename):
        with open(filename, 'rb') as f:
            data = pickle.load(f)
        address_book = cls()
        address_book.data = data
        return address_book

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __set__(self, instance, value):
        if not value.isdigit():
            raise ValueError("Phone number must contain only digits.")
        super().__set__(instance, value)

class Birthday(Field):
    def __set__(self, instance, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Incorrect date format. Use YYYY-MM-DD.")
        super().__set__(instance, value)

class Record:
    def __init__(self, name_value, birthday_value=None):
        self.name = Name(name_value)
        self.birthday = Birthday(birthday_value) if birthday_value else None
        self.phones = []

    def add_phone(self, phone_value):
        phone = Phone(phone_value)
        self.phones.append(phone)

    def remove_phone(self, phone_value):
        for phone in self.phones:
            if phone.value == phone_value:
                self.phones.remove(phone)
                break

    def edit_phone(self, old_value, new_value):
        for phone in self.phones:
            if phone.value == old_value:
                phone.value = new_value
                break

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now()
            next_birthday = datetime(today.year, self.birthday.month, self.birthday.day)
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, self.birthday.month, self.birthday.day)
            days_left = (next_birthday - today).days
            return days_left
        else:
            return None