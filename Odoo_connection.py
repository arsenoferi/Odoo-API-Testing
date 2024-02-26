import requests
import json

class Odoo_connection():
    
    def __init__(self, url,db,username,password):
        self.url = url
        self.db = db
        self.username = username
        self.password = password
        self.headers = {'Content-Type': 'application/json'}
    
    def test_connection(self):
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "common",
                "method": "login",
                "args": [self.db, self.username, self.password],
            },
            "id": 1,
        }

        response = requests.post(self.url, data=json.dumps(payload), headers=self.headers)
        uid = response.json().get("result")

        if uid:
            print("Successfully authenticated. UID:", uid)
            self.uid = uid
        else:
            print("Authentication failed.")
    
    def odoo_get_data(self,model,domain=[],fields_att=[]):
        data_payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [
                    self.db, self.uid, self.password,
                    f'{model}',  # Model
                    'search_read',  # Method
                    domain,  # Domain (empty array for all records)
                    {'fields': fields_att}  # Fields to fetch
                ],
            },
            "id": 2,
        }
        response = requests.post(self.url, data=json.dumps(data_payload), headers=self.headers)
        data = response.json().get("result", [])
        return data
        

    def odoo_get_column(self,model):
        fields_payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [
                    self.db, self.uid, self.password,
                    f'{model}',  # Model name
                    'fields_get',  # Method to list all fields
                    [],  # No arguments for fields_get
                    {'attributes': ['string', 'help', 'type','readonly','states']} # Context (optional)
                ],
            },
            "id": 2,  # Arbitrary ID
        }
        response = requests.post(self.url, data=json.dumps(fields_payload), headers=self.headers)
        fields_info = response.json().get("result")
        return fields_info