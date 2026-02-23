from datetime import datetime, timedelta

frmt = '%Y-%m-%dT%H:%M:%S'

eventindexes_to_remove = []

def eventPostProcess(event, index):
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

    unknowns = {}

    for line in lines:
        #print(lineIndex, lines[lineIndex])
        if line.startswith("BEGIN:VEVENT"):
            currentEventIndex += 1
            returnOBJ["events"].append({
                "room": "?",
                "building": "?",
                "location": "?",
            })
        elif line.startswith("END:VEVENT"):
            eventPostProcess(returnOBJ["events"][currentEventIndex], currentEventIndex)
            unknown = []
            for c in ["room", "building", "location"]:
                if returnOBJ["events"][currentEventIndex][c] == "?": unknown.append(c)

            if len(unknown) > 1 and not returnOBJ["events"][currentEventIndex]["summary"] in unknowns:
                unknowns[returnOBJ["events"][currentEventIndex]["summary"]] = unknown

        elif line.startswith("SUMMARY"):
            returnOBJ["events"][currentEventIndex]["summary"] = "-".join(line.split("-")[1:])[1:]
            returnOBJ["events"][currentEventIndex]["type"] = line.split(':', 1)[1][0]
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
            if len(desc.split("\\", 1)[0].split(" ", 1)) > 1: returnOBJ["events"][currentEventIndex]["room"] = desc.split("\\", 1)[0].split(" ", 1)[1]
            if len(desc.split("[", 1)) > 1: returnOBJ["events"][currentEventIndex]["building"] = desc.split("[", 1)[1].split("]", 1)[0]
        elif line.startswith("STATUS"):
            returnOBJ["events"][currentEventIndex]["status"] = line.split(":")[1]
        elif line.startswith("LOCATION"):
            if len(line.split(":", 1)) > 1: returnOBJ["events"][currentEventIndex]["location"] = "".join(line.split(":", 1)[1].split("\\"))
        elif line.startswith("DTSTAMP") and returnOBJ["dtstamp"] is None:
            returnOBJ["dtstamp"] = formatDate(line.split(":")[-1])

        elif line.startswith("X-WR-TIMEZONE"):
            returnOBJ["timezone"] = line.split(":")[1]

        lineIndex += 1

    if len(unknowns) > 0:
        print("WARNING> Couldn't get information about this events")
        print(unknowns)
        input("Continue?")

    eventindexes_to_remove.sort(reverse=True)

    for i in range(len(eventindexes_to_remove)):
        print("removed from list", returnOBJ["events"].pop(eventindexes_to_remove[i]))

    return returnOBJ

def formatDate(unformatted):
    return f"{unformatted[:4]}-{unformatted[4:6]}-{unformatted[6:8]}T{unformatted[9:11]}:{unformatted[11:13]}:{unformatted[13:15]}"

#to test module
if __name__ == "__main__":
    print(parseIcal("plan.ics"))