import json
import csv
from datetime import date
from HabitAnalyzer import DailyHabit, HabitRecord, HabitAnalyzer

FILE_NAME = "habits.json"


def save_data(analyzer):
    data = []

    for habit in analyzer.habits:
        records = []
        for r in habit.records:
            records.append({
                "date": r.date.isoformat(),
                "done": r.done
            })

        data.append({
            "name": habit.name,
            "records": records
        })

    with open(FILE_NAME, "w") as f:
        json.dump(data, f)


def load_data():
    try:
        with open(FILE_NAME, "r") as f:
            data = json.load(f)

        habits = []
        for h in data:
            habit = DailyHabit(h["name"])
            for r in h["records"]:
                habit.add_record(
                    HabitRecord(
                        date.fromisoformat(r["date"]),
                        r["done"]
                    )
                )
            habits.append(habit)

        return HabitAnalyzer(habits)

    except FileNotFoundError:
        return None


def export_csv(analyzer):
    with open("habits.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Habit", "Date", "Done"])

        for habit in analyzer.habits:
            for r in habit.records:
                writer.writerow([habit.name, r.date, r.done])