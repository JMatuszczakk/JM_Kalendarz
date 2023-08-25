# This is a simple calendar app for sharing with my family
import streamlit as st
import pandas as pd

# Create a .csv file that will contain the calendar
try:
    df = pd.read_csv("calendar.csv")
except:
    df = pd.DataFrame(columns=["Date", "Event"])
    df.to_csv("calendar.csv", index=False)

st.title('Kalendasz')

with st.form('dodaj_wydarzenie'):
    st.subheader('Dodaj wydarzenie')
    event_name = st.text_input('Nazwa wydarzenia', key='event_name')
    event_date = st.date_input('Data wydarzenia', key='event_date')
    submit_button = st.form_submit_button(label='Dodaj wydarzenie')
    if submit_button:
        new_row = pd.DataFrame({"Date": [event_date], "Event": [event_name]})
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv("calendar.csv", index=False)
        st.success('Wydarzenie dodane!')

# Convert DataFrame entries to calendar_events format
calendar_events = []
for _, row in df.iterrows():
    calendar_event = {
        "title": row["Event"],
        "start": str(row["Date"]),  # Convert the date to string format
        "end": str(row["Date"]),    # Convert the date to string format
    }
    calendar_events.append(calendar_event)

# Display the interactive calendar
from streamlit_calendar import calendar

# Specify the options to show a week view
calendar_options = {
    "initialView": "dayGridWeek",  # Set the view to "week"
    "locale": "pl",                # Set locale to Polish
    "firstDay": 1
}

# Create the calendar widget using the dynamically generated events and options
calendar_widget = calendar(events=calendar_events, options=calendar_options)

try:
    st.toast(calendar_widget['eventClick']['event']['title'])
except:
    pass

# Display the calendar widget
st.write(calendar_widget)
