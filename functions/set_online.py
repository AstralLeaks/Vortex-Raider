import websocket
import json

def set_status(token, status):
        ws = websocket.WebSocket()
        ws.connect('wss://gateway.discord.gg/?v=9&encoding=json')
        ws.send(json.dumps({
            'op': 2,
            'd': {
                'token': token,
                'properties': {
                    '$os': 'windows',
                    '$browser': 'Discord',
                    '$device': 'desktop' },
                'presence': {
                    'status': status,
                    'since': 0,
                    'activities': [],
                    'afk': False } } }))
        
while True:
    set_status('nigger', 'dnd')

"""
                        'online',
                        'dnd',
                        'idle'])
                        """