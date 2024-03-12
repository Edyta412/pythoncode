
from abc import ABC, abstractmethod
import re
import pickle
from datetime import datetime, timedelta


class Field:
    """Base class for entry fields."""

    def __init__(self, value):
        self.value = value


class Name(Field):
    """Class for first and last name."""

    pass


class Phone(Field):
    """Class for phone number with validation."""

    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError("Niepoprawny numer telefonu")
        super().__init__(value)

    @staticmethod
    def validate_phone(value):
        """Checks if the phone number is valid (9 digits, format 123456789)."""
        pattern = re.compile(r"^\d{9}$")
        return pattern.match(value) is not None


class Email(Field):
    """Class for email address with validation."""

    def __init__(self, value):
        if not self.validate_email(value):
            raise ValueError("Niepoprawny adres email")
        super().__init__(value)

    @staticmethod
    def validate_email(value):
        """Checks if the email is valid."""
        pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        return pattern.match(value) is not None


class Birthday(Field):
    """Class for birthday with validation."""

    def __init__(self, value):
        if not self.validate_birthday(value):
            raise ValueError("Niepoprawna data urodzenia")
        super().__init__(value)

    @staticmethod
    def validate_birthday(value):
        """Checks if the birthday is valid."""
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return True
        except ValueError:
            return False


class Address(Field):
    """Class for residential address."""

    def __init__(self, street, city, postal_code, country):
        self.street = street
        self.city = city
        self.postal_code = postal_code
        self.country = country
        super().__init__(f"{street}, {city}, {postal_code}, {country}")


class Record:
    """Class for an entry in the address book."""

    def __init__(self, name: Name, birthday: Birthday = None, address: Address = None):
        self.name = name
        self.phones = []
        self.emails = []
        self.birthday = birthday
        self.address = address
        self.notes = []

    def add_phone(self, phone: Phone):
        """Adds a phone number."""
        self.phones.append(phone)

    def remove_phone(self, phone: Phone):
        """Removes a phone number."""
        self.phones.remove(phone)

    def edit_phone(self, old_phone: Phone, new_phone: Phone):
        """Changes a phone number."""
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def add_email(self, email: Email):
        """Adds an email address."""
        self.emails.append(email)

    def remove_email(self, email: Email):
        """Removes an email address."""
        self.emails.remove(email)

    def edit_email(self, old_email: Email, new_email: Email):
        """Changes an email address."""
        self.remove_email(old_email)
        self.add_email(new_email)

    def edit_name(self, new_name: Name):
        """Changes the first and last name."""
        self.name = new_name

    def days_to_birthday(self):
        """Returns the number of days to the next birthday."""
        if not self.birthday or not self.birthday.value:
            return "Brak daty urodzenia"
        today = datetime.now()
        bday = datetime.strptime(self.birthday.value, "%Y-%m-%d")
        next_birthday = bday.replace(year=today.year)
        if today > next_birthday:
            next_birthday = next_birthday.replace(year=today.year + 1)
        days = (next_birthday - today).days
        return days

    def edit_address(self, new_address: Address):
        """Changes the address."""
        self.address = new_address

    def __str__(self):
        """Returns a string representation of the entry, now including address."""
        phones = ", ".join(phone.value for phone in self.phones)
        emails = ", ".join(email.value for email in self.emails)
        birthday_str = f", Urodziny: {self.birthday.value}" if self.birthday else ""
        days_to_bday_str = (
            f", Dni do urodzin: {self.days_to_birthday()}" if self.birthday else ""
        )
        address_str = f", Adres: {self.address.value}" if self.address else ""
        return (
            f"Imię i nazwisko: {self.name.value}, "
            f"Telefony: {phones}, Email: {emails}{birthday_str}{days_to_bday_str}{address_str}"
        )

    def add_note(self, note):
        """Adds a note to the record."""
        self.notes.append(note)

    def show_notes(self):
        """Shows all notes associated with the record."""
        if not self.notes:
            print("No notes for this contact.")
        else:
            print("Notes:")
            for note in self.notes:
                print(note)


class AddressBook(UserDict):
    """Class for the address book."""

    def add_record(self, record: Record):
        """Adds an entry to the address book."""
        self.data[record.name.value] = record
        print("Dodano wpis.")

    def show_all_records(self):
        if not self.data:
            print("Brak kontaktów")
        else:
            print("Kontakty: ")
            for i, (name, record) in enumerate(self.data.items(), start=1):
                print(f"{i}. {name}: {record}")

    def find_record(self, search_term):
        """Finds entries containing the exact phrase provided."""
        found_records = []
        for record in self.data.values():
            if search_term.lower() in record.name.value.lower():
                found_records.append(record)
                continue
            for phone in record.phones:
                if search_term in phone.value:
                    found_records.append(record)
                    break
            for email in record.emails:
                if search_term in email.value:
                    found_records.append(record)
                    break
        return found_records

    def upcoming_birthdays(self, days):
        today = datetime.now().date()
        days = int(days)
        print(today)
        upcoming_birthdays = []
        for record in self.data.values():
            if record.birthday:

                bday = datetime.strptime(record.birthday.value, "%Y-%m-%d").date()
                print(bday)
                next_birthday = bday.replace(year=today.year)
                if today > next_birthday:
                    next_birthday = next_birthday.replace(year=today.year + 1)

                days_to = (next_birthday - today).days
                print(days_to)
                if (next_birthday - today).days <= days:
                    upcoming_birthdays.append(record.name.value)

        element = ", ".join(upcoming_birthdays)
        print(f"W ciągu najblizszych {days} dni, urodziny mają: \n{element}")

    def delete_record(self, name):
        """Deletes a record by name."""
        if name in self.data:
            del self.data[name]
            print(f"Usunięto wpis: {name}.")
        else:
            print(f"Wpis o nazwie {name} nie istnieje.")

    def __iter__(self):
        """Returns an iterator over the address book records."""
        self.current = 0
        return self

    def __next__(self):
        if self.current < len(self.data):
            records = list(self.data.values())[self.current : self.current + 5]
            self.current += 5
            return records
        else:
            raise StopIteration

    def find_by_birthday_range(self, days):
        """Finds contacts with birthdays within the specified range of days."""
        found_contacts = []
        for record in self.data.values():
            days_to_birthday = record.days_to_birthday()
            if (
                days_to_birthday != "Brak daty urodzenia"
                and 0 <= days_to_birthday <= days
            ):
                found_contacts.append(record)
        return found_contacts


def edit_record(book):
    """Edits an existing record in the address book."""
    name_to_edit = input("Wprowadź imię i nazwisko które chcesz edytować: ")
    if name_to_edit in book.data:
        record = book.data[name_to_edit]
        print(f"Edytowanie: {name_to_edit}.")

        new_name_input = input(
            "Podaj imię i nazwisko (wciśnij Enter żeby zachować obecne): "
        )
        if new_name_input.strip():
            record.edit_name(Name(new_name_input))
            print("Zaktualizowano imię i nazwisko.")

        if record.phones:
            print("Obecne numery telefonów: ")
            for idx, phone in enumerate(record.phones, start=1):
                print(f"{idx}. {phone.value}")
            phone_to_edit = input(
                "Wprowadź indeks numeru telefonu który chcesz edytować "
                "(wciśnij Enter żeby zachować obecny): "
            )
            if phone_to_edit.isdigit():
                idx = int(phone_to_edit) - 1
                if 0 <= idx < len(record.phones):
                    new_phone_number = input("Podaj nowy numer telefonu: ")
                    if new_phone_number.strip():
                        record.edit_phone(record.phones[idx], Phone(new_phone_number))
                        print("Numer telefonu zaktualizowany.")
                    else:
                        print("Nie dokonano zmian.")
                else:
                    print("Niepoprawny indeks numeru.")
            else:
                print("Pomięto edycję numeru.")
        else:
            print("Brak numerów telefonu.")

        print("Wpis zaktualizowany.")
    else:
        print("Wpisu nie znaleziono.")


def save_address_book(book, filename="address_book.pkl"):
    try:
        with open(filename, "wb") as file:
            pickle.dump(book.data, file)
        print("Zapisano liste adresową.")
    except Exception as e:
        print(f"Błąd przy zapisie liście kontaktów: {e}")


def load_address_book(filename="address_book.pkl"):
    try:
        with open(filename, "rb") as file:
            data = pickle.load(file)
        book = AddressBook()
        book.data = data
        print("Witam w Osobistym asystencie.")
        return book
    except FileNotFoundError:
        print("Plik nie istnieje, tworzenie nowej listy kontaktów.")
        return AddressBook()
    except Exception as e:
        print(f"Błąd przy ładowaniu listy kontaktów: {e}")
        return AddressBook()


def input_phone():
    """Asks the user to enter a phone number."""
    while True:
        try:
            number = input(
                "Podaj numer telefonu (9 cyfr): ")
            return Phone(number)
        except ValueError as e:
            print(e)


def input_email():
    """Asks the user to enter an email address."""
    while True:
        try:
            email = input(
                "Podaj adres email: ")
            return Email(email)
        except ValueError as e:
            print(e)


def input_birthday():
    """Asks the user to enter a birthday."""
    while True:
        try:
            birthday = input(
                "Podaj datę urodzenia (RRRR-MM-DD): ")
            return Birthday(birthday)
        except ValueError as e:
            print(e)


def input_address():
    """Asks the user to enter an address."""
    street = input("Podaj ulicę: ")
    city = input("Podaj miasto: ")
    postal_code = input("Podaj kod pocztowy: ")
    country = input("Podaj kraj: ")
    return Address(street, city, postal_code, country)


class UserInterface(ABC):
    """Abstract base class for user interfaces."""

    @abstractmethod
    def display_menu(self):
        """Display the main menu."""
        pass

    @abstractmethod
    def get_user_input(self):
        """Get user input."""
        pass

    @abstractmethod
    def display_message(self, message):
        """Display a message to the user."""
        pass

    @abstractmethod
    def display_contacts(self, contacts):
        """Display a list of contacts."""
        pass

    @abstractmethod
    def display_contact_details(self, contact):
        """Display details of a contact."""
        pass


class ConsoleInterface(UserInterface):
    """User interface implementation for console."""

    def display_menu(self):
        print("\nMenu:")
        print("1. Dodaj kontakt")
        print("2. Pokaż wszystkie kontakty")
        print("3. Znajdź kontakt")
        print("4. Edytuj kontakt")
        print("5. Usuń kontakt")
        print("6. Zapisz listę kontaktów")
        print("7. Wczytaj listę kontaktów")
        print("8. Zakończ")
        print("9. Opcje dodatkowe")

    def get_user_input(self, prompt):
        return input(prompt)

    def display_message(self, message):
        print(message)

    def display_contacts(self, contacts):
        if not contacts:
            print("Brak pasujących kontaktów.")
        else:
            for i, contact in enumerate(contacts, start=1):
                print(f"{i}. {contact}")

    def display_contact_details(self, contact):
        print(contact)


def main():
    ui = ConsoleInterface()
    address_book = load_address_book()

    while True:
        ui.display_menu()
        choice = ui.get_user_input("Wybierz opcję: ")

        if choice == "1":
            name_input = ui.get_user_input("Podaj imię i nazwisko: ")
            new_record = Record(Name(name_input))
            new_record.add_phone(input_phone())
            new_record.add_email(input_email())
            new_record.birthday = input_birthday()
            new_record.address = input_address()
            address_book.add_record(new_record)

        elif choice == "2":
            address_book.show_all_records()

        elif choice == "3":
            search_term = ui.get_user_input("Wprowadź frazę do wyszukania: ")
            found_contacts = address_book.find_record(search_term)
            ui.display_contacts(found_contacts)

        elif choice == "4":
            edit_record(address_book)

        elif choice == "5":
            name_to_delete = ui.get_user_input("Wprowadź imię i nazwisko do usunięcia: ")
            address_book.delete_record(name_to_delete)

        elif choice == "6":
            save_address_book(address_book)

        elif choice == "7":
            address_book = load_address_book()

        elif choice == "8":
            print("Dziękujemy. Do widzenia!")
            break

        elif choice == "9":
            days = ui.get_user_input("Podaj liczbę dni: ")
            address_book.upcoming_birthdays(days)


if __name__ == "__main__":
    main()
