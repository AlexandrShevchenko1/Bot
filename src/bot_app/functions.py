
def retrieveWeekEventsData(jsonString):
    response = ""
    for i in jsonString:
        for item in jsonString[f"{i}"]:
            if (len(item) == 0): break
            response += f"*Event:* _{item['id']}_"
            response += f"*\nName:* _{item['name']}_"
            response += f"*\nLocation:* _{item['place']}_\n"
            response += f"*Category:* _{item['category']}_\n\n"
    return response


def retrieveDayEventData(jsonString):
    response = ""
    for event in jsonString:
        response += f"\n*Name:* _{event['name']}_"
        response += f"\n*Location:* _{event['place']}_\n"
        response += f"*Category:* _{event['category']}_\n\n"
    return response
