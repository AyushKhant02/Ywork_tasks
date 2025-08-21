# core/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.utils import timezone

from .models import Employee
from .mongo import get_collection

class DepartmentChatConsumer(AsyncWebsocketConsumer):
    """
    Connect with: ws://host/ws/chat/?employee_id=1
    - Finds the employee and its department
    - Uses department UUID as group name
    - Saves messages to MongoDB with group as partition key
    """

    async def connect(self):
        # Simple demo auth: employee_id in query string (replace with real auth/JWT if needed)
        self.employee_id = self.scope["query_string"].decode().split("employee_id=")[-1] if b"employee_id=" in self.scope["query_string"] else None
        if not self.employee_id:
            await self.close(code=4401)  # unauthorized
            return

        emp = await self._get_employee(self.employee_id)
        if not emp:
            await self.close(code=4404)  # not found
            return

        # Group name = department UUID (as required)
        self.group_name = str(emp.department_id)
        self.emp_name = emp.name
        self.emp_pk = emp.id

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # Optional: notify join
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat.message",
                "payload": {
                    "system": True,
                    "message": f"{self.emp_name} joined",
                    "employeeId": self.emp_pk,
                    "ts": timezone.now().isoformat(),
                },
            },
        )

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        try:
            data = json.loads(text_data or "{}")
            message = (data.get("message") or "").strip()
        except Exception:
            message = ""

        if not message:
            return

        doc = {
            "group": self.group_name,              # partition key
            "employeeId": self.emp_pk,
            "employeeName": self.emp_name,
            "message": message,
            "ts": timezone.now().isoformat(),
        }

        # Save to MongoDB
        await sync_to_async(self._save_to_mongo)(doc)

        # Broadcast to the whole department group
        await self.channel_layer.group_send(
            self.group_name,
            {"type": "chat.message", "payload": doc},
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["payload"]))

    @sync_to_async
    def _get_employee(self, emp_id: str):
        try:
            return Employee.objects.select_related("department").get(id=int(emp_id))
        except Employee.DoesNotExist:
            return None

    def _save_to_mongo(self, doc: dict):
        coll = get_collection()
        coll.insert_one(doc)
