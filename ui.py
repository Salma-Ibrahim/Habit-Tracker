import streamlit as st
from datetime import date
from HabitAnalyzer import DailyHabit, HabitRecord, HabitAnalyzer
from storage import save_data, load_data, export_csv

st.set_page_config(
    page_title="Habit Tracker",
    layout="centered"
)

# ------------------------------
# Initialize habits (Session State)
# ------------------------------
if "analyzer" not in st.session_state:
    loaded = load_data()
    if loaded:
        st.session_state.analyzer = loaded
    else:
        st.session_state.analyzer = HabitAnalyzer([
            DailyHabit("Drink Water"),
            DailyHabit("Exercise"),
            DailyHabit("Reading")
        ])

analyzer = st.session_state.analyzer
today = date.today()

# ==============================
# Sidebar (Controls)
# ==============================
with st.sidebar:
    st.title("⚙️ Controls")

    st.subheader("Add New Habit")
    new_habit_name = st.text_input(
        "Habit name",
        placeholder="e.g. Meditate, Walk 5k steps"
    )

    if st.button("Add Habit", use_container_width=True):
        if new_habit_name.strip():
            existing = [h.name.lower() for h in analyzer.habits]
            if new_habit_name.lower() in existing:
                st.warning("Habit already exists.")
            else:
                analyzer.habits.append(DailyHabit(new_habit_name))
                save_data(analyzer)
                st.success("Habit added successfully.")
                st.rerun()
        else:
            st.warning("Please enter a habit name.")

    st.divider()

    if st.button("Export to CSV", use_container_width=True):
        export_csv(analyzer)
        st.success("Exported as habits.csv")

    if st.button("Reset All Data", use_container_width=True):
        st.session_state.clear()
        st.rerun()
st.subheader("Delete Habit")
if analyzer.habits:
    habit_to_delete = st.selectbox(
        "Select habit to delete",
        [h.name for h in analyzer.habits]
    )

    if st.button("Delete Habit", use_container_width=True):
        # Remove habit from list
        analyzer.habits = [
            h for h in analyzer.habits if h.name != habit_to_delete
        ]
        save_data(analyzer)
        st.success(f"Habit '{habit_to_delete}' deleted successfully.")
        st.rerun()
else:
    st.caption("No habits available to delete.")

# ==============================
# Main Page
# ==============================
st.title("Personal Habit Tracker")

st.caption("Track daily habits, measure consistency, and build streaks.")

# ------------------------------
# Today's Habits
# ------------------------------
st.subheader("Today's Habits")

if not analyzer.habits:
    st.info("No habits yet. Add one from the sidebar.")
else:
    for habit in analyzer.habits:
        with st.container(border=True):
            col1, col2 = st.columns([1, 4])

            with col1:
                done = st.checkbox(
                    habit.name,
                    key=f"{habit.name}_{today}"
                )

            with col2:
                habit.add_record(HabitRecord(today, done))
                save_data(analyzer)

                st.progress(habit.success_rate() / 100)
                st.caption(
                    f"Success rate: {habit.success_rate():.1f}% • "
                    f"Current streak: {habit.get_streak()} days"
                )

# ------------------------------
# Summary Section
# ------------------------------
st.subheader("Summary")

col1, col2 = st.columns(2)

best = analyzer.best_habit()
worst = analyzer.worst_habit()

with col1:
    st.metric(
        "Best Habit",
        best.name if best else "—",
        f"{best.success_rate():.1f}%" if best else None
    )

with col2:
    st.metric(
        "Needs Attention",
        worst.name if worst else "—",
        f"{worst.success_rate():.1f}%" if worst else None
    )

st.subheader("Highest Commitment Days")
commitment = analyzer.highest_commitment_days()

if commitment:
    for day, count in sorted(commitment.items()):
        st.write(f"{day} — {count} habits completed")
else:
    st.caption("No commitment data yet.")