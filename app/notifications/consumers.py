import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Grupo único para cada usuario basado en su ID
        self.group_name = f'notifications_{self.scope["user"].id}'
        
        # Unirse al grupo de notificaciones del usuario
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        
        await self.accept()

    async def disconnect(self, close_code):
        # Abandonar el grupo de notificaciones del usuario
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # Recibir mensaje del grupo de canales
    async def send_notification(self, event):
        # Enviar mensaje al cliente
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'message': event['message'],
        }))