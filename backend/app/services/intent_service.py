import json
import re
from typing import Optional
from urllib import error, request

from app.core.config import settings


class IntentService:
    CREATE_KEYWORDS = ("create", "add", "register", "new user", "sign up")
    LIST_KEYWORDS = ("list", "show all", "all users", "users list")
    GET_KEYWORDS = ("get user", "show user", "find user", "fetch user", "user details")
    UPDATE_KEYWORDS = ("update", "edit", "change", "modify")
    DELETE_KEYWORDS = ("delete", "remove")

    def detect_intent(self, message: str) -> str:
        llm_intent = self._detect_intent_with_groq(message)
        if llm_intent:
            return llm_intent

        normalized = message.lower().strip()

        if any(keyword in normalized for keyword in self.CREATE_KEYWORDS):
            return "create_user"
        if any(keyword in normalized for keyword in self.LIST_KEYWORDS):
            return "list_users"
        if any(keyword in normalized for keyword in self.DELETE_KEYWORDS):
            return "delete_user"
        if any(keyword in normalized for keyword in self.UPDATE_KEYWORDS):
            return "update_user"
        if any(keyword in normalized for keyword in self.GET_KEYWORDS):
            return "get_user"

        return "unknown"

    def extract_user_id(self, message: str) -> Optional[int]:
        match = re.search(r"\b(\d+)\b", message)
        if not match:
            return None
        return int(match.group(1))

    def extract_update_fields(self, message: str) -> dict:
        lowered = message.lower()
        updates = {}

        patterns = {
            "name": r"name\s+(?:to|is)?\s*([a-zA-Z ]+)",
            "age": r"age\s+(?:to|is)?\s*(\d+)",
            "gender": r"gender\s+(?:to|is)?\s*([a-zA-Z]+)",
            "address": r"address\s+(?:to|is)?\s*([\w\s,.-]+)",
            "phone_number": r"(?:phone|phone number|mobile)\s+(?:to|is)?\s*(\d{10,15})",
        }

        for field, pattern in patterns.items():
            match = re.search(pattern, lowered)
            if not match:
                continue

            value = match.group(1).strip()
            if field == "age":
                updates[field] = int(value)
            else:
                updates[field] = value

        return updates

    def _detect_intent_with_groq(self, message: str) -> Optional[str]:
        if not settings.GROQ_API_KEY:
            return None

        payload = {
            "model": settings.GROQ_MODEL,
            "temperature": 0,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Classify the user request into exactly one intent from this list: "
                        "create_user, get_user, list_users, update_user, delete_user, unknown. "
                        "Respond only with compact JSON like {\"intent\":\"create_user\"}."
                    ),
                },
                {"role": "user", "content": message},
            ],
        }

        req = request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=8) as response:
                body = json.loads(response.read().decode("utf-8"))
        except (error.URLError, TimeoutError, json.JSONDecodeError):
            return None

        try:
            content = body["choices"][0]["message"]["content"]
            parsed = json.loads(content)
            intent = parsed.get("intent")
        except (KeyError, IndexError, TypeError, json.JSONDecodeError):
            return None

        allowed = {"create_user", "get_user", "list_users", "update_user", "delete_user", "unknown"}
        return intent if intent in allowed else None


intent_service = IntentService()
