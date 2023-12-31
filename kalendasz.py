# This is a simple calendar app for sharing with my family
import streamlit as st
import pandas as pd
from supabase import create_client, Client
#import datetime
from datetime import datetime, timedelta
import simplepush

# Connect to the database

@st.cache_resource
def init_connection():
    url = st.secrets["supabase_url"]
    key = st.secrets["supabase_key"]
    return create_client(url, key)

supabase = init_connection()




# Create a cursor object
# Fetch all the records
result = supabase.table('events').select('*').execute()
#format is ('data', [{'id': 1, 'event_name': 'test1', 'event_date_start': None, 'event_date_end': '2023-08-25 20:05:52'}])

#format of result.data is
# [{
#   "id": 1,
#   "event_name": "test1",
#   "event_date_start": null,
#   "event_date_end": "2023-08-25 20:05:52"
# },
# {
#   "id": 2,
#   "event_name": "makapaka1",
#   "event_date_start": "2023-08-25T21:15:00",
#   "event_date_end": "2023-08-25T22:15:00"
# }
# ]


#create df from result.data
df = pd.DataFrame(result.data)
df = df.rename(columns={'event_name': 'ev_name', 'event_date_start': 'ev_date_start', 'event_date_end': 'ev_date_stop'})

print(df)
st.title('Kalendasz')
st.subheader("Nadchodzące wydarzenia")
upc = []
for i in result.data:
    #convert i['event_date_start'] to datetime
    datetime_object = datetime.strptime(i['event_date_start'], '%Y-%m-%dT%H:%M:%S')
    #if datetime_object is today or after:
    if datetime_object >= datetime.today():
        ttt = ""
        #if date is today show "Dzisiaj, o " + time
        #if date is tommorow show "Jutro, o " + time
        #else show date and day of the week + time
        if datetime_object.date() == datetime.today().date():
            ttt = "Dzisiaj, o " + datetime_object.strftime("%H:%M")
        elif datetime_object.date() == datetime.today().date() + timedelta(days=1):
            ttt = "Jutro, o " + datetime_object.strftime("%H:%M")
        else:
            ttt = datetime_object.strftime("%A, %d %B %Y, %H:%M")
        upc.append({'Nazwa wydażenia': i['event_name'], 'Data i czas': ttt})
st.table(upc)

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
        supabase.table('events').insert([{'event_name': event_name, 'event_date_start': event_str_start, 'event_date_end': event_str_stop}]).execute()
        st.success('Wydarzenie dodane')
        st.balloons()
        simplepush.send(key='uSndSj', title='Dodano nowe wydarzenie', message='Dodano wydarzenie: ' + event_name + ' na dzień ' + str(event_date) + ' o godzinie ' + str(event_time) + '.')
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

print(calendar_events)

# Display the interactive calendar
from streamlit_calendar import calendar

# Specify the options to show a week view
calendar_options = {
    "initialView": "timeGridWeek",  # Set the view to "week"
    "locale": "pl",                # Set locale to Polish
    "right": "dayGridWeek, timeGridDay",
}
calendar_widget = calendar(events=calendar_events, options=calendar_options)

calendar_options2 = {
    "initialView": "timeGridDay",  # Set the view to "week"
    "locale": "pl",                # Set locale to Polish
    #set shown date to calendar_widget['dateClick']['date']
}
calendar_widget2 = calendar(events=calendar_events, options=calendar_options2)

try:
    st.toast(calendar_widget['eventClick']['event']['title'])
    st.write(calendar_widget['eventClick']['event']['title'])
except:
    pass
# Create the calendar widget using the dynamically generated events and options

       


