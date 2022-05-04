import requests
import json

INVALID_TOKEN='No Token'
roboats_Token= INVALID_TOKEN
roboats_url='https://roboats.virtualregatta.com/api'

def checkStatus(response,name='',debug=False):
    if debug:
        if response.status_code==200 :
            print('Request '+name+' success')

        else :
            print('Request '+name+' failed')
            if response.status_code==404:
                print('\t'+response.text)
            else:
                print('\t'+response.json()['error']['message'])
                print('\t'+response.json()['error']['type'],' | ',response.json()['error']['code'])
    try :
        return response.json()
    except ValueError :
        return response.headers

def login(mail="deepazurteam@outlook.com",password="4CAJHW",raceId=531,legNum=1,debug=False):
    global roboats_Token,roboats_url
    bodyLogin = json.dumps({
        "email": mail,
        "password": password,
        "raceId": raceId,
        "legNum": legNum
    })
    headersLogin = {
        'Content-Type': 'application/json'
    }
    logingUrl = "%s/login" % roboats_url
    response = requests.request("POST", logingUrl, headers=headersLogin, data=bodyLogin)
    if response.status_code == 200:
        roboats_Token=response.headers['Token']
    else :
        roboats_Token=INVALID_TOKEN
    return checkStatus(response,name="login",debug=debug)

def InfosFast(debug=False):
    global roboats_Token,roboats_url
    infoFastUrl = "%s/infos/fast" % roboats_url
    payload = ""
    headers = {
        'Token': roboats_Token
    }
    response = requests.request("GET", infoFastUrl, headers=headers, data=payload)
    return checkStatus(response,name="infoFast",debug=debug)

def InfosSlow(debug=False):
    global roboats_Token,roboats_url
    infoFastUrl = "%s/infos/slow" % roboats_url
    payload = ""
    headers = {
        'Token': roboats_Token
    }
    response = requests.request("GET", infoFastUrl, headers=headers, data=payload)
    return checkStatus(response,name="infoSlow",debug=debug)

def BoatActions(tsLegStart:int,actions:list,debug=False):
    """
    :param tsLegStart: Timestamp of the actions
    :param actions: list of a dict of the actions like :
        actions =[
                {
                    "type": "heading",
                    "values": {
                        "deg": 200,
                        "autoTwa": True
                    }
                }
            ]
    :param debug: boolean to show debug or not
    :return: response (dict)
    """
    global roboats_Token, roboats_url
    boatActionstUrl = "%s/boat/actions" % roboats_url
    payload = json.dumps({
        "tsLegStart": tsLegStart,
        "actions": actions
    })
    headers = {
        'Token':roboats_Token,
        'Content-Type': 'application/json'
    }

    response = requests.request("PUT", boatActionstUrl, headers=headers, data=payload)
    return checkStatus(response,name="Boat Action",debug=debug)

def main():
    global roboats_Token, roboats_url
    login(debug=1)
    TS=1651686030000
    action = [{
          "type": "heading",
          "values": {
            "deg": 200,
            "autoTwa": True}}]


    info=BoatActions(TS,action,debug=True)
    print(info)




if __name__ == '__main__':
    main()


