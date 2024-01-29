
from collections import UserDict

class AddressBook(UserDict):
    def find_records(self, search_term):
        results = []
        for record in self.values():
            if search_term.lower() in record.name.value.lower():
                results.append(record)
        return results

    def __setitem__(self, key, record):
        self.data[key] = record

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    pass


class Record:
    def __init__(self, name_value):
        self.name = Name(name_value)
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

address_book = AddressBook()
record1 = Record("John Doe")
record1.add_phone("123-456-789")
record1.add_phone("987-654-321")

record2 = Record("Jane Smith")
record2.add_phone("555-123-456")

address_book["john_doe"] = record1
address_book["jane_smith"] = record2

search_results = address_book.find_records("john")

for result in search_results:
    print(result.name, result.phones)