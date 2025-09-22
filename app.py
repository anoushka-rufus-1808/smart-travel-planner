import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from budget_utils import compute_per_day, build_itinerary

st.title("Smart Travel Planner & Expense Tracker")

tab1, tab2 = st.tabs(["Itinerary Planner", "Expense Tracker"])

# ---------------- ITINERARY ----------------
with tab1:
    st.header("Plan your trip")
    budget = st.number_input("Total budget (₹)", min_value=0, value=10000)
    days = st.number_input("No. of days", min_value=1, value=3)
    style = st.selectbox("Travel style", ["cheap","standard","luxury"])
    destination = st.text_input("Destination", "Shimla")

    if st.button("Generate itinerary"):
        per_day = compute_per_day(budget, days)
        st.write(f"Per-day budget: ₹{per_day}")

        activities = pd.read_csv("data/activities.csv").to_dict(orient="records")
        itinerary, remaining = build_itinerary(days, activities, per_day, style)

        for day, acts in itinerary.items():
            st.subheader(day)
            if acts:
                for a in acts:
                    st.write(f"- {a['name']} (₹{a['cost']})")
            else:
                st.write("No activities added.")

        st.success("Itinerary generated!")

# ---------------- EXPENSES ----------------
with tab2:
    st.header("Track expenses")
    try:
        expenses = pd.read_csv("data/expenses.csv")
    except FileNotFoundError:
        expenses = pd.DataFrame(columns=["date","category","desc","amount"])

    st.dataframe(expenses)

    with st.form("add_expense"):
        d = st.date_input("Date")
        cat = st.selectbox("Category", ["transport","food","stay","activity","misc"])
        desc = st.text_input("Description")
        amt = st.number_input("Amount", min_value=0)
        if st.form_submit_button("Add"):
            new = {"date":d, "category":cat, "desc":desc, "amount":amt}
            expenses = expenses.append(new, ignore_index=True)
            expenses.to_csv("data/expenses.csv", index=False)
            st.experimental_rerun()

    if not expenses.empty:
        grouped = expenses.groupby("category")["amount"].sum()
        fig, ax = plt.subplots()
        grouped.plot(kind="bar", ax=ax)
        ax.set_ylabel("Amount (₹)")
        st.pyplot(fig)
