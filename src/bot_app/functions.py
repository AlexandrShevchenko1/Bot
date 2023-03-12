from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import List, Collection

from dateutil import parser


def retrieveWeekEventsData(jsonString) -> str:
    response: List[str] = []
    for i in jsonString:
        for item in jsonString[f"{i}"]:
            if (len(item) == 0):
                break
            # response += f"*Event:* _{item['id']}_"
            response.extend((
                f"*\nName:* _{item['name']}_",
                f"*\nLocation:* _{item['place']}_\n",
                f"*Category:* _{item['category']}_\n",
                f"*Start:* _{parser.parse(item['start']).strftime('%d-%m-%Y')}_\n",
                f"*End:* _{parser.parse(item['start']).strftime('%d-%m-%Y')}_\n",
                f"*Group:* \n"
            ))

            participant_groups: Collection = item['participant_groups']
            if (len(participant_groups) == 0):
                response.append(f"_-_\n")
            else:
                response.extend((f"_{g['name']}_\n" for g in participant_groups))
    
    return "".join(response)


def retrieveDayEventData(jsonString)-> str:
    response: List[str] = []
    for event in jsonString:
        response.extend((
            f"\n*Name:* _{event['name']}_",
            f"\n*Location:* _{event['place']}_\n",
            f"*Category:* _{event['category']}_\n\n",
            f"*Start:* _{parser.parse(event['start']).strftime('%d-%m-%Y')}_\n",
            f"*End:* _{parser.parse(event['start']).strftime('%d-%m-%Y')}_\n",
            f"*Group:* \n"
        ))

        participant_groups: Collection = event['participant_groups']
        if (len(participant_groups) == 0):
            response.append(f"_-_\n")
        else:
            response.extend((f"_{g['name']}_\n" for g in participant_groups))

    return "".join(response)

def retrieveUserData(jsonString) -> str:
    response: List[str] = []

    for user in jsonString:
        response.extend((
            f"*Id:* _{user['id']}_\n",
            f"*UserName:* _{user['username']}_\n",
            f"\n*Group:* "
        ))

        participant_groups: Collection = user['participant_groups']
        if (len(participant_groups) == 0):
            response.append(f"_-_\n")
        else:
            response.extend((f"_{g['name']}_\n" for g in participant_groups))
        # response += f"*Group:* _{user['participant_groups'][0]['name']}_\n"

        response.append(
            f"\n_{user['username']} is professor_" \
            if (user['is_staff']) else \
            f"\n_{user['username']} is student_"
        )

    return "".join(response)

def retrieveEventData(events) -> str:
    response: List[str] = []
    
    for event in events:
        print(event['id'])
        response.append(f"/edit + id + name + groupName\n(use *-* symbol to skip parameter)\n\nEvent *id*: {event['id']}\n\nAvailable fields to change:")
        # response += f"\n*Id:* _{event['id']}_"
        response.append(f"\n*Name:* _{event['name']}_")
        # response += f"\n*Category:* _{event['category']}_"
        response.extend((f"\n*Group:* _{g['name']}_\n" for g in event['participant_groups']))
        #datetime.datetime.strptime(event['end'],'%Y-%m-%d').date()
        #end = datetime.datetime.strptime(f"{event['end']}", '%d-%m-%Y').strftime('%d-%m-%Y')
        #start = datetime.datetime.strptime(f"{event['start']}", '%d-%m-%Y').strftime('%d-%m-%Y')
        #response += f"*Start:* _{start}_\n\n"
        #response += f"*End:* _{end}_\n"
    
    return "".join(response)
