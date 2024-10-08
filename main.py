from datetime import datetime, timezone, timedelta
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import urllib.request

from modules.icalParser import parseIcal
from modules.gauth import auth

import yaml
import os.path

if not os.path.isfile('config.yaml'):
    print("please rename and configure example-config.yaml to config.yaml")
    exit()

# Load YAML config file
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# ical url, OPTIONAL - it is to update current file
icalUrl = config['icalUrl']

# filename for ical
filename = config['filename']

# If modifying these scopes, delete the file token.json.
SCOPES = config['scopes']

# if to skip updating already exisiting events
skipUpdating = config['skipUpdating']

# calendar to append and edit
calendarId = config['calendarId']

# Modify to set colors, available:
"""
1 blue
2 green
3 purple
4 red
5 yellow
6 orange
7 turquoise
8 gray
9 bold blue
10 bold green
11 bold red
"""
COLORS = config['colors']

frmt = '%Y-%m-%dT%H:%M:%S'

def main():

    if icalUrl is not None and not (icalUrl == ""):
        urllib.request.urlretrieve(icalUrl, filename)
    else:
        if not os.path.isfile(filename):
            return print("You must provide working ical link or file with correct filename.")

    #getting calendar from ical file
    calendar = parseIcal(filename)
    print("starting stamp", calendar['dtstamp'])

    #using gcalendar api
    creds = auth(SCOPES)

    try:
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        now = datetime.now(timezone.utc).isoformat()[:26] + "Z"  # 'Z' indicates UTC time
        print("Getting the upcoming 1000 events...")
        events_result = (
            service.events()
            .list(
                calendarId=calendarId,
                timeMin=yesterday(calendar['dtstamp']) + "Z",
                maxResults=1000,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        collidingEvents = {}

        if not events:
            print("No upcoming events found.")
        else:
            # Prints the start and name of the next 10 events
            for event in events:
                #print(event)
                date = event['start']['dateTime'][:19]
                collidingEvents[date] = {"id": event['id'], "summary": event["summary"]}

        #print(collidingEvents)


        # Create a batch request object
        batch = service.new_batch_http_request(callback=batch_callback)

        print("adding/updating events, can take a minute...")
        if skipUpdating:
            print("  Skipping updating")

        #add events
        for evt in calendar["events"]:
            title = f"{evt['building'][:1] + evt['building'][2:]}/{evt['room']} {evt['summary']}"
            event = {
                'summary': title,
                'location': evt["location"],
                'description': evt["description"],
                'start': {
                    'dateTime': evt["dtstart"],
                    'timeZone': calendar["timezone"],
                },
                'end': {
                    'dateTime': evt["dtend"],
                    'timeZone': calendar["timezone"],
                },
                'colorId': getColor(evt["type"])
            }
            if evt["dtstart"] in collidingEvents:
                if not skipUpdating:
                    batch.add(service.events().update(calendarId=calendarId, eventId=collidingEvents[evt["dtstart"]]["id"], body=event))
            else:
                batch.add(service.events().insert(calendarId=calendarId, body=event))

        batch.execute()

    except HttpError as error:
        print(f"An error occurred: {error}")

# Batch request callback handler
def batch_callback(request_id, response, exception):
    if exception:
        print(f"Request {request_id} failed: {exception}")
    else:
        print(f"Request {request_id} succeeded: {response}")

def getColor(colorName):
    col = COLORS[colorName]
    if col:
        return col
    return 1

def yesterday(dateString):
    datetime_object = datetime.strptime(dateString, frmt) - timedelta(days=1, hours=2)
    return datetime_object.strftime(frmt)

if __name__ == "__main__":
    main()