# pwr-google-calendar-sync
Syncing calendar from pwr USOS ical url/file to google calendar using api


## Installing and configuration
1. `git clone https://github.com/kyanbasu/pwr-google-calendar-sync.git`

2. `pip install -r requirements.txt`

3. Copy/rename example-config.yaml to config.yaml and configure it.

## Running
Run `main.py`

## More
There are helper scripts to configure (`gcalendarinfo.py`) or delete many events (`bulkdelete.py`)

> [!CAUTION]
> I do not take responsibility for miss deleting/changing/creating too many events - though it shouldn't happen. Please read code before you use it.
