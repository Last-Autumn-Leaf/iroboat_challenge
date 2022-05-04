import requests
import json
import argparse

class Roboat_API:
    #class variable
    INVALID_TOKEN = 'No Token'
    INVALID_RESP=dict()
    roboats_url = 'https://roboats.virtualregatta.com/api'
    mail = "deepazurteam@outlook.com"
    password = "Hidden"
    debug=False

    def __init__(self,raceId=531,legNum=1,debug=None):
        self.INVALID_TOKEN = 'No Token'
        self.roboats_url = 'https://roboats.virtualregatta.com/api'
        self.mail = "deepazurteam@outlook.com"
        self.password = "4CAJHW"

        self.token = self.INVALID_TOKEN
        self.raceId = raceId
        self.legNum = legNum
        if debug!=None :
            self.debug=debug

        #------- Try to log ------
        self.login()

    def checkStatus(self,response, name=''):
        if self.debug:
            if response.status_code == 200:
                print('Request ' + name + ' success')

            else:
                print('Request ' + name + ' failed')
                if response.status_code == 404:
                    print('\t' + response.text)
                else:
                    print('\t' + response.json()['error']['message'])
                    print('\t' + response.json()['error']['type'], ' | ', response.json()['error']['code'])
        try:
            return response.json()
        except ValueError:
            return response.headers

    def login(self):

        bodyLogin = json.dumps({
            "email": self.mail,
            "password": self.password,
            "raceId": self.raceId,
            "legNum": self.legNum
        })
        headersLogin = {
            'Content-Type': 'application/json'
        }
        logingUrl = "%s/login" % self.roboats_url
        response = requests.request("POST", logingUrl, headers=headersLogin, data=bodyLogin)
        if response.status_code == 200:
            self.token = response.headers['Token']
        else:
            self.token = self.INVALID_TOKEN
        return self.checkStatus(response, name="login")

    def InfosFast(self):
        if self.token == self.INVALID_TOKEN :
            print('Invalid Token, trying to reconnect')
            self.login()
            if self.token == self.INVALID_TOKEN :
                print("reconnection failed...")
                return self.INVALID_RESP
            else :
                self.InfosFast()
        else:
            infoFastUrl = "%s/infos/fast" % self.roboats_url
            payload = ""
            headers = {
                'Token': self.token
            }
            response = requests.request("GET", infoFastUrl, headers=headers, data=payload)
            return self.checkStatus(response, name="infoFast")

    def InfosSlow(self):
        if self.token == self.INVALID_TOKEN :
            print('Invalid Token, trying to reconnect')
            self.login()
            if self.token == self.INVALID_TOKEN :
                print("reconnection failed...")
                return self.INVALID_RESP
            else :
                self.InfosSlow()
        else :
            infoFastUrl = "%s/infos/slow" % self.roboats_url
            payload = ""
            headers = {
                'Token': self.token
            }
            response = requests.request("GET", infoFastUrl, headers=headers, data=payload)
            return self.checkStatus(response,name="infoSlow")

    def BoatActions(self,tsLegStart: int, actions: list):
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
        :return: response (dict)
        """
        if self.token == self.INVALID_TOKEN :
            print('Invalid Token, trying to reconnect')
            self.login()
            if self.token == self.INVALID_TOKEN :
                print("reconnection failed...")
                return self.INVALID_RESP
            else :
                self.BoatActions()
        else :
            boatActionstUrl = "%s/boat/actions" % self.roboats_url
            payload = json.dumps({
                "tsLegStart": tsLegStart,
                "actions": actions
            })
            headers = {
                'Token': self.token,
                'Content-Type': 'application/json'
            }

            response = requests.request("PUT", boatActionstUrl, headers=headers, data=payload)
            return self.checkStatus(response, name="Boat Action")

if __name__ == '__main__':
    #password should not be writtin in clear
    #this is an attempt to hide it

    parser = argparse.ArgumentParser("API_interface")
    parser.add_argument("--password", help="Password for connection", type=str)
    args = parser.parse_args()
    Roboat_API.password=args.password
    api_caller= Roboat_API()
    print(api_caller.token)
