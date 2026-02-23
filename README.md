# pwr-google-calendar-sync
Syncing calendar from PWr USOS ical url/file to google calendar using api

## But why? There is already option to export and sync calendar directly to other service from USOS
I know USOS already has a sync option, but it honestly isn't great. Everything ends up being the same color, and the titles aren't very helpful. I wanted something that uses Google's colored blocks and tells me exactly where and what the room is at a glance. 

Plus, USOS data is sometimes just wrong - this way, I can set my own rules to fix the event timing or descriptions whenever I need to.

## Installing
```sh
git clone https://github.com/kyanbasu/pwr-google-calendar-sync.git
cd pwr-google-calendar-sync
pip install -r requirements.txt
```
Using uv
```sh
uv pip install -r requirements.txt
```

## Configuration

1. Create App on Google Cloud, enable Google Calendar API, create OAuth credentials.

2. Download them as JSON, rename them to `credentials.json` and put into the root directory of project.

3. Duplicate `example-config.yaml` and rename to `config.yaml`.

4. (Optional) On USOS on calendar page click export, copy link and paste it as icalUrl in `config.yaml` so it does auto sync.

    4.5. If url in previous step wasn't set you need to manually get ical file and rename it to one set in `config.yaml`.

5. After Google verifies Your project run `gcalendarinfo.py`, verify with google and using provided information you can configure `config.yaml`.

> [!TIP]
> I advice creating separate calendar for these events to not break any event in primary. After creating one, run `gcalendarinfo.py` to get calendarId and set it in `config.yaml`.

## Running
### Helpers
There are helper scripts to configure (`gcalendarinfo.py`) or delete many events (`bulkdelete.py`) - by default it deletes only future and events which are in ical file, so theoretically it shouldn't remove important and manually edited events.

### Independent event rules
You can insert rules to post process in event parser, function `eventPostProcess` in `modules/icalParser.py`

Example:
```py
def eventPostProcess(event, index):
    #print(event)
    if event['summary'] == "Niezawodność i diagnostyka układów cyfrowych 2" and event['type'] == "P":
        event['dtstart'] = (datetime.strptime(event['dtstart'], frmt) + timedelta(minutes=30)).strftime(frmt) # Offsets start of event with defined name and type
    elif event['summary'] == "Inżynierskie zastosowania statystyki" and event['type'] == "C":
        event['dtstart'] = (datetime.strptime(event['dtstart'], frmt) + timedelta(minutes=15)).strftime(frmt) # Offsets start of event with only name defined
    elif event['summary'] == "Fizyka 3.1":
        eventindexes_to_remove.append(index) # Doesn't add event to calendar
    pass
```

### Updating calendar
Run `main.py`

> [!CAUTION]
> I do not take responsibility for miss deleting/changing/creating too many events - though it shouldn't happen. Please read code before you use it.
> This is why it is adviced to use separate calendarId
