import json
from datetime import datetime
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


with open("1399478eva-data.json", "r", encoding="utf-8") as file:
    eva_data = json.load(file)

records = []


def parse_duration_hours(duration_text):
    if not duration_text or ":" not in duration_text:
        return None

    try:
        hours, minutes = map(int, duration_text.split(":"))
        return hours + minutes / 60
    except ValueError:
        return None


# classify data into short standard and long
def categorise_eva_by_length(records):
    short = 0
    standard = 0
    long = 0

    for _, duration_hours in records:
        if duration_hours < 4.0:
            short += 1
        elif duration_hours < 7.0:
            standard += 1
        else:
            long += 1

    total_records = short + standard + long

    if total_records == 0:
        return {
            "short": {"count": 0, "percentage": 0.0},
            "standard": {"count": 0, "percentage": 0.0},
            "long": {"count": 0, "percentage": 0.0},
        }

    return {
        "short": {"count": short, "percentage": (short / total_records) * 100},
        "standard": {"count": standard, "percentage": (standard / total_records) * 100},
        "long": {"count": long, "percentage": (long / total_records) * 100},
    }


# stores the total EVA duration for each country
total_eva_hours_by_country = {}

# stores the number of EVAs recorded for each country
eva_count_by_country = {}

skipped_records = 0

for eva in eva_data:
    if not isinstance(eva, dict):
        skipped_records += 1
        continue

    date_text = eva.get("date")
    duration_text = eva.get("duration")
    country_name = eva.get("country")

    if not date_text or not duration_text:
        skipped_records += 1
        continue

    try:
        date = datetime.fromisoformat(date_text)
    except ValueError:
        skipped_records += 1
        continue

    duration_hours = parse_duration_hours(duration_text)
    if duration_hours is None:
        skipped_records += 1
        continue

    records.append((date, duration_hours))

    if country_name:
        if country_name not in total_eva_hours_by_country:
            total_eva_hours_by_country[country_name] = 0
        total_eva_hours_by_country[country_name] += duration_hours

        if country_name not in eva_count_by_country:
            eva_count_by_country[country_name] = 0
        eva_count_by_country[country_name] += 1

records.sort(key=lambda record: record[0])

dates = []
cumulative_hours = []
total_hours = 0.0

for date, duration_hours in records:
    total_hours += duration_hours
    dates.append(date)
    cumulative_hours.append(total_hours)

if dates:
    plt.figure()
    plt.plot(dates, cumulative_hours)
    plt.xlabel("Year")
    plt.ylabel("Cumulative EVA duration (hours)")
    plt.tight_layout()
    plt.savefig("cumulative_duration.png")
    plt.close()

category_summary = categorise_eva_by_length(records)
print("EVA category breakdown:")
for category_name in ("short", "standard", "long"):
    category_data = category_summary[category_name]
    print(
        f"{category_name}: count={category_data['count']}, "
        f"percentage={category_data['percentage']:.2f}%"
    )

print(f"Skipped invalid rows: {skipped_records}")

selected_country_name = input("Enter country: ").strip()

if selected_country_name in total_eva_hours_by_country:
    average_eva_hours = (
        total_eva_hours_by_country[selected_country_name]
        / eva_count_by_country[selected_country_name]
    )

    print(
        f"Number of EVAs for {selected_country_name} is "
        f"{eva_count_by_country[selected_country_name]}"
    )
    print(
        f"Total EVA duration for {selected_country_name} is "
        f"{total_eva_hours_by_country[selected_country_name]:.2f} hours"
    )
    print(
        f"Average EVA duration for {selected_country_name} is "
        f"{average_eva_hours:.2f} hours"
    )
else:
    print(f"No EVA records found for {selected_country_name}")
