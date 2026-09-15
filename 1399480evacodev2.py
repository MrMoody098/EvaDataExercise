import json
from datetime import datetime

import matplotlib.pyplot as plt

with open("data.json", "r", encoding="utf-8") as file:
    eva_data = json.load(file)

records = []

# Stores the total EVA duration for each country
total_eva_hours_by_country = {}

# Stores the number of EVAs recorded for each country
eva_count_by_country = {}

for eva in eva_data:
    date_text = eva.get("date")
    duration_text = eva.get("duration")

    # Gets the country associated with the current EVA record
    country_name = eva.get("country")

    if not date_text or not duration_text:
        continue

    date = datetime.fromisoformat(date_text)
    hours, minutes = map(int, duration_text.split(":"))
    duration_hours = hours + minutes / 60

    records.append((date, duration_hours))

    # Adds the current EVA duration to the total for its country
    if country_name:
        if country_name not in total_eva_hours_by_country:
            total_eva_hours_by_country[country_name] = 0

        total_eva_hours_by_country[country_name] += duration_hours

        # Counts the number of valid EVAs for each country
        if country_name not in eva_count_by_country:
            eva_count_by_country[country_name] = 0

        eva_count_by_country[country_name] += 1

records.sort(key=lambda record: record[0])

dates = []
cumulative_hours = []
total_hours = 0

for date, duration_hours in records:
    total_hours += duration_hours
    dates.append(date)
    cumulative_hours.append(total_hours)

plt.plot(dates, cumulative_hours)
plt.xlabel("Year")
plt.ylabel("Cumulative EVA duration (hours)")
plt.tight_layout()
plt.savefig("cumulative_duration.png")
plt.show()


# Allows the user to choose which country's EVA statistics to display
selected_country_name = input("Enter country: ")

# Displays the statistics if the selected country exists in the data
if selected_country_name in total_eva_hours_by_country:
    # Calculates the average EVA duration using the total duration and EVA count
    average_eva_hours = (
        total_eva_hours_by_country[selected_country_name]
        / eva_count_by_country[selected_country_name]
    )

    print(
        "Number of EVAs for",
        selected_country_name,
        "is",
        eva_count_by_country[selected_country_name],
    )
    print(
        "Total EVA duration for",
        selected_country_name,
        "is",
        total_eva_hours_by_country[selected_country_name],
        "hours",
    )
    print(
        "Average EVA duration for",
        selected_country_name,
        "is",
        average_eva_hours,
        "hours",
    )
else:
    print("No EVA records found for", selected_country_name)
