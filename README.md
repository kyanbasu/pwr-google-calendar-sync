# pwr-google-calendar-sync
Syncing calendar from pwr USOS ical url/file to google calendar using api


## Installing
1. `git clone https://github.com/kyanbasu/pwr-google-calendar-sync.git`

2. `pip install -r requirements.txt`

## Configuration

1. Create App on Google Cloud, enable Google Calendar API, create OAuth credentials.

2. Download them as JSON, rename them to credentials.json and put into the root directory of project.

3. Duplicate example-config.yaml and rename to config.yaml.

4. (Optionally) On USOS on calendar page click export, copy link and paste it as icalUrl in config.yaml.

5. After Google verifies Your project run gcalendarinfo.py, verify with google and using returned information configure config.json.

## Running
### Helpers
There are helper scripts to configure (`gcalendarinfo.py`) or delete many events (`bulkdelete.py`)

### Updating calendar
Run `main.py`

> [!CAUTION]
> I do not take responsibility for miss deleting/changing/creating too many events - though it shouldn't happen. Please read code before you use it.
