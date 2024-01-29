from datetime import datetime, timedelta

users = [
    {"name": "Bill", "birthday": datetime(2023, 1, 9)},
    {"name": "Jill", "birthday": datetime(2023, 1, 10)},
    {"name": "Kim", "birthday": datetime(2023, 1, 13)},
    {"name": "Jan", "birthday": datetime(2023, 1, 14)},
]

def get_birthdays_per_week(users):
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    week_ago = start_of_week - timedelta(days=7)
    birthday_users = [user["name"] for user in users if week_ago <= user["birthday"] < start_of_week]

    grouped_birthdays = {}
    for user in users:
        if week_ago <= user["birthday"] < start_of_week:
            day_of_week = user["birthday"].strftime("%A")
            if day_of_week not in grouped_birthdays:
                grouped_birthdays[day_of_week] = []
            grouped_birthdays[day_of_week].append(user["name"])

    for day, names in grouped_birthdays.items():
        print(f"{day}: {', '.join(names)}")

get_birthdays_per_week(users)