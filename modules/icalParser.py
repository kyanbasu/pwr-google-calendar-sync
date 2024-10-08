from datetime import datetime, timedelta

frmt = '%Y-%m-%dT%H:%M:%S'

def eventPostProcess(event):
    #print(event)
    pass

def parseIcal(name):
    """
    :param name: name of file
    :type name: str
    returns object with parsed events and timezone, parameters:
     timezone - timezone string, e.g "Europe/Warsaw"

     dtstamp - start time of ical

     events - array of event objects
    event object:
     summary - name of event

     type - type of subject, W - wykład, P - projekt, L - laboratorium, C - ćwiczenia

     dtstart - start datetime

     dtend - end datetime

     description

     location

     room

     building

     status
    """
    f = open(name, "r", encoding="utf-8")

    lines = []

    returnOBJ = {"timezone": None, "dtstamp": None, "events": []}

    currentEventIndex = -1

    lineIndex = 0

    lines = f.read().splitlines()

    for line in lines:
        #print(lineIndex, lines[lineIndex])
        if line.startswith("BEGIN:VEVENT"):
            currentEventIndex += 1
            returnOBJ["events"].append({})
        elif line.startswith("END:VEVENT"):
            eventPostProcess(returnOBJ["events"][currentEventIndex])
        elif line.startswith("SUMMARY"):
            returnOBJ["events"][currentEventIndex]["summary"] = "-".join(line.split("-")[1:])[1:]
            returnOBJ["events"][currentEventIndex]["type"] = line.split(':')[1][0]
        elif line.startswith("DTSTART"):
            returnOBJ["events"][currentEventIndex]["dtstart"] = formatDate(line.split(":")[-1])
        elif line.startswith("DTEND"):
            returnOBJ["events"][currentEventIndex]["dtend"] = formatDate(line.split(":")[-1])
        elif line.startswith("DESCRIPTION"):
            i = 1
            while lines[lineIndex + i].startswith(" "):
                line += lines[lineIndex + i][1:]
                i += 1
            desc = ":".join(line.split(":")[1:])
            returnOBJ["events"][currentEventIndex]["description"] = desc.replace("\\n", "\n")
            returnOBJ["events"][currentEventIndex]["room"] = desc.split("\\")[0].split(" ")[1]
            returnOBJ["events"][currentEventIndex]["building"] = desc.split("[")[1].split("]")[0] if len(desc.split("[")) > 1 else None
        elif line.startswith("STATUS"):
            returnOBJ["events"][currentEventIndex]["status"] = line.split(":")[1]
        elif line.startswith("LOCATION"):
            returnOBJ["events"][currentEventIndex]["location"] = "".join(line.split(":")[1].split("\\"))
        elif line.startswith("DTSTAMP") and returnOBJ["dtstamp"] is None:
            returnOBJ["dtstamp"] = formatDate(line.split(":")[-1])

        elif line.startswith("X-WR-TIMEZONE"):
            returnOBJ["timezone"] = line.split(":")[1]

        lineIndex += 1

    return returnOBJ

def formatDate(unformatted):
    return f"{unformatted[:4]}-{unformatted[4:6]}-{unformatted[6:8]}T{unformatted[9:11]}:{unformatted[11:13]}:{unformatted[13:15]}"

#to test module
if __name__ == "__main__":
    print(parseIcal("plan.ics"))