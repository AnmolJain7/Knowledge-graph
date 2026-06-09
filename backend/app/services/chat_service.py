import re


class ChatService:

    def update_state_from_message(self, state: dict, message: str): 
        cleaned_message = message.strip()

        current_step = state.get("current_step")

        if current_step == "collect_name":
            state["name"] = cleaned_message
            state["response"] = None

        elif current_step == "collect_age":
            extracted_number = self._extract_first_number(cleaned_message)
            try:
                state["age"] = int(extracted_number) if extracted_number is not None else int(cleaned_message)
                state["response"] = None
            except ValueError:
                state["response"] = "Age should be a number. Please enter a valid age."

        elif current_step == "collect_gender":
            state["gender"] = cleaned_message
            state["response"] = None

        elif current_step == "collect_address":
            state["address"] = cleaned_message
            state["response"] = None

        elif current_step == "collect_phone":
            digits_only = "".join(ch for ch in cleaned_message if ch.isdigit())
            if len(digits_only) < 10:
                state["response"] = "Phone number should have at least 10 digits. Please re-enter it."
            else:
                state["phone_number"] = digits_only
                state["response"] = None

        elif current_step == "collect_user_id":
            extracted_number = self._extract_first_number(cleaned_message)
            try:
                state["user_id"] = int(extracted_number) if extracted_number is not None else int(cleaned_message)
                state["response"] = None
            except ValueError:
                state["response"] = "User id should be a number. Please enter a valid user id."

        state["last_user_message"] = cleaned_message

        return state

    def _extract_first_number(self, message: str):
        match = re.search(r"\b(\d+)\b", message)
        if not match:
            return None
        return match.group(1)


chat_service = ChatService()
