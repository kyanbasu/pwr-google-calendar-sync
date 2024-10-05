from datetime import datetime, timezone
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from gauth import auth

SCOPES = ["https://www.googleapis.com/auth/calendar"]

if __name__ == "__main__":
    # using gcalendar api
    creds = auth(SCOPES)

    try:
        service = build("calendar", "v3", credentials=creds)

        colors = service.colors().get().execute()

        print("\nAvailable colors:")

        # Print available calendarListEntry colors.
        print(colors)
        for id, color in colors['calendar'].items():
            print('colorId: %s' % id)
            print('  Background: %s' % color['background'])
            print('  Foreground: %s' % color['foreground'])
        # Print available event colors.
        for id, color in colors['event'].items():
            print('colorId: %s' % id)
            print('  Background: %s' % color['background'])
            print('  Foreground: %s' % color['foreground'])


        print("\nCalendars")
        print("name\t\t\tid")
        page_token = None
        while True:
            calendar_list = service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                print(calendar_list_entry['summary'], "\t\t\t", calendar_list_entry['id'])
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break




    except HttpError as error:
        print(f"An error occurred: {error}")