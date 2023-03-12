import datetime


from dateutil import parser

def retrieveWeekEventsData(jsonString):
    response = ""
    for i in jsonString:
        for item in jsonString[f"{i}"]:
            if (len(item) == 0): break
            # response += f"*Event:* _{item['id']}_"
            response += f"*\nName:* _{item['name']}_"
            response += f"*\nLocation:* _{item['place']}_\n"
            response += f"*Category:* _{item['category']}_\n"
            response += f"*Start:* _{parser.parse(item['start']).strftime('%d-%m-%Y')}_\n"
            response += f"*End:* _{parser.parse(item['start']).strftime('%d-%m-%Y')}_\n"
            response += f"*Group:* \n"
            if (len(item['participant_groups']) == 0):
                response += f"_-_\n"
            else:
                for g in item['participant_groups']:
                    response += f"_{g['name']}_\n"
    return response


def retrieveDayEventData(jsonString):
    response = ""
    for event in jsonString:
        response += f"\n*Name:* _{event['name']}_"
        response += f"\n*Location:* _{event['place']}_\n"
        response += f"*Category:* _{event['category']}_\n\n"
        response += f"*Start:* _{parser.parse(event['start']).strftime('%d-%m-%Y')}_\n"
        response += f"*End:* _{parser.parse(event['start']).strftime('%d-%m-%Y')}_\n"
        response += f"*Group:* \n"
        if (len(event['participant_groups']) == 0):
            response += f"_-_\n"
        else:
            for g in event['participant_groups']:
                response += f"_{g['name']}_\n"
    return response

def retrieveUserData(jsonString):
    response = ""

    for user in jsonString:
        response += f"*Id:* _{user['id']}_\n"
        response += f"*UserName:* _{user['username']}_\n"
        response += f"\n*Group:* "

        if (len(user['participant_groups']) == 0):
            response += f"_-_\n"
        else:
            for g in user['participant_groups']:
                response += f"_{g['name']}_\n"
        # response += f"*Group:* _{user['participant_groups'][0]['name']}_\n"

        if (user['is_staff']):
            response += f"\n_{user['username']} is professor_"
        else:

            response += f"\n_{user['username']} is student_"

    return response



def retrieveEventData(events):
    response = ""
    
    for event in events:
        print(event['id'])
        response += f"/edit + id + name + groupName\n(use *-* symbol to skip parameter)\n\nEvent *id*: {event['id']}\n\nAvailable fields to change:"
        # response += f"\n*Id:* _{event['id']}_"
        response += f"\n*Name:* _{event['name']}_"
        # response += f"\n*Category:* _{event['category']}_"
        for g in event['participant_groups']:
            response += f"\n*Group:* _{g['name']}_\n"
        #datetime.datetime.strptime(event['end'],'%Y-%m-%d').date()
        #end = datetime.datetime.strptime(f"{event['end']}", '%d-%m-%Y').strftime('%d-%m-%Y')
        #start = datetime.datetime.strptime(f"{event['start']}", '%d-%m-%Y').strftime('%d-%m-%Y')
        #response += f"*Start:* _{start}_\n\n"
        #response += f"*End:* _{end}_\n"
    return response
