from fastapi import WebSocket
from typing import List


class ConnectionManager:

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):

        """
        Aceita conexão e adiciona na lista ativa
        """
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):

        """
        Remove conexão da lista ativa
        """
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):

        """
        Envia mensagem apenas para um cliente
        """
        await websocket.send_text(message)

    async def broadcast(self, message: str):

        """
        Envia mensagem para todos os clientes conectados
        """
        for connection in self.active_connections:
            await connection.send_text(message)


class WebSocketService:

    def __init__(self):
        self.manager = ConnectionManager()

    async def handle_connection(self, websocket: WebSocket):

        """
        Gerencia ciclo completo da conexão WebSocket
        """

        await self.manager.connect(websocket)

        try:
            while True:

                # recebe mensagem do cliente
                message = await websocket.receive_text()

                # broadcast para todos conectados
                await self.manager.broadcast(message)

        except Exception:
            # remove conexão em caso de erro ou desconexão
            self.manager.disconnect(websocket)

            await self.manager.broadcast(
                "⚠️ Um usuário desconectou"
            )

    async def notify_user(self, websocket: WebSocket, message: str):

        """
        Notificação direta para um usuário específico
        """
        await self.manager.send_personal_message(message, websocket)

    async def notify_all(self, message: str):

        """
        Notificação global para todos usuários
        """
        await self.manager.broadcast(message)