# This is a simple calendar app for sharing with my family
import streamlit as st
import pandas as pd
import mysql as mysql
import mysql.connector
from mysql.connector import Error

# Connect to the database
try:
    connection = mysql.connector.connect(
        host='sql.freedb.tech',
        user='freedb_jmatuszczak',
        password='E!Z&2jE87Nc9CSX',
        database='freedb_jmkalendarz',

    )
except Error as e:
    print(e)

    
# Create a cursor object
cursor = connection.cursor()
cursor.execute("SELECT * FROM kalendarz")
# Fetch all the records
result = cursor.fetchall()
# Print the result
for row in result:
    print(row)

#create df from result
df = pd.DataFrame(result, columns=['id', 'ev_name', 'ev_date_start', 'ev_date_stop'])

st.title('Kalendasz')

with st.form('dodaj_wydarzenie'):
    st.subheader('Dodaj wydarzenie')
    event_name = st.text_input('Nazwa wydarzenia', key='event_name')
    event_date = st.date_input('Data wydarzenia', key='event_date')
    event_time = st.time_input('Godzina wydarzenia', key='event_time')
    event_stop_time = st.time_input('Godzina zakończenia wydarzenia', key='event_stop_time')
    submit_button = st.form_submit_button(label='Dodaj wydarzenie')
    event_str_start = str(event_date) + 'T' + str(event_time)
    event_str_stop = str(event_date) + 'T' + str(event_stop_time)
    if submit_button:
        cursor.execute("INSERT INTO kalendarz (ev_name, ev_date_start, ev_date_stop) VALUES (%s, %s, %s)", (event_name, event_str_start, event_str_stop))
        connection.commit()
        st.success('Wydarzenie dodane')
        st.balloons()
        st.experimental_rerun()

# Convert DataFrame entries to calendar_events format
calendar_events = []
for _, row in df.iterrows():
    calendar_event = {
        "title": row["ev_name"],
        "start": str(row["ev_date_start"]),  # Convert the date to string format
        "end": str(row["ev_date_stop"]),    # Convert the date to string format
    }
    calendar_events.append(calendar_event)
print(calendar_event)

# Display the interactive calendar
from streamlit_calendar import calendar

# Specify the options to show a week view
calendar_options = {
    "initialView": "timeGridWeek",  # Set the view to "week"
    "locale": "pl",                # Set locale to Polish
    "right": "dayGridWeek, timeGridDay",
}
calendar_widget = calendar(events=calendar_events, options=calendar_options)
st.write(calendar_widget)

calendar_options2 = {
    "initialView": "timeGridDay",  # Set the view to "week"
    "locale": "pl",                # Set locale to Polish
    "slotMaxTime": "00:00:00",
    #set shown date to calendar_widget['dateClick']['date']
}


try:
    st.toast(calendar_widget['eventClick']['event']['title'])
except:
    pass
# Create the calendar widget using the dynamically generated events and options



# Display the calendar widget

