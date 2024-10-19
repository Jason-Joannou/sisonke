import json
from typing import Dict, List, Optional, Tuple, Union, cast

from database.state_manager.queries import (
    check_if_unregistered_state_exists,
    get_current_pool_selection,
    get_state_responses,
    pop_previous_state,
    set_current_pool_selection,
    update_current_state,
)
from database.users.queries import check_if_number_exists_sqlite
from whatsapp_utils.api_requests import query_endpoint
from whatsapp_utils.schemas.state_schema import StateSchema
from whatsapp_utils.state_config import MESSAGE_STATES
from whatsapp_utils.twilio_messenger import send_conversational_message


class MessageStateManager:

    # We handle registration outside, this is purely for state management
    def __init__(self, user_number: str) -> None:
        self.base_greetings = MESSAGE_STATES["base_state"]
        self.unrecognized_state = MESSAGE_STATES["unrecognized_state"]
        self.user_number = user_number
        self.registration_status = self.check_registration_status()
        self.current_state_tag: Optional[str] = None
        self.current_state: Union[Dict, StateSchema] = {}
        self.update_local_states()

    def check_registration_status(self) -> bool:
        return check_if_number_exists_sqlite(from_number=self.user_number)

    def update_registration_status(self):
        if not self.registration_status:
            self.registration_status = self.check_registration_status()

    def processes_user_request(self, user_action: str) -> str:
        self.update_registration_status()
        # User is not registered
        if not self.registration_status:
            if user_action in self.base_greetings:
                self.set_current_state(tag="unregistered_number")
                return self.get_current_state_message()

            # Need to validate their wallet
            # if user_action not in self.get_current_state_valid_actions():
            #     return self.get_unrecognized_state_response()

            action_requests = self.get_current_state_action_requests()
            endpoint = action_requests.get("1")
            msg = self.execute_action_request(
                endpoint=endpoint,
                payload={
                    "user_input": user_action,
                    "user_number": self.user_number,
                    "current_pool": self.get_current_pool_selection(),
                },
            )
            return self.return_twilio_formatted_message(msg=msg)

        check_if_unregistered_state_exists(from_number=self.user_number)
        self.update_local_states()
        if user_action in self.base_greetings:
            self.set_current_state(tag="registered_number")
            return self.get_current_state_message()

        if (
            self.current_state_tag is None
            and user_action not in self.get_current_state_valid_actions()
        ):
            return self.get_unrecognized_state_response()
        # Check if action is valid for the current state
        if (
            self.current_state_tag is not None
            and "input_request" not in self.current_state_tag
            and user_action not in self.get_current_state_valid_actions()
        ):
            return self.get_unrecognized_state_response()

        # Validation for input state
        if (
            isinstance(self.current_state_tag, str)
            and "input_request" in self.current_state_tag
        ):
            flag, user_input = self.handle_input_state_validation(
                user_input=user_action
            )
            if not flag:
                # If false we want execution to stop, if true we want execution to carry on
                msg = self.current_state["invalid_message"]
                self.set_previous_state()  # Need to move back to state before
                return self.return_twilio_formatted_message(msg=msg)

        # Check if we need to transfer state
        # Back is also a transerable state
        if self.get_current_state_state_selections():  # We have to transfer state

            # Check if selection is a back state selection
            if user_action in self.current_state["state_selection"].keys():
                if self.current_state["state_selection"][user_action] == "back_state":
                    self.set_previous_state()
                    return self.get_current_state_message()

                if self.get_current_pool_in_state():
                    pools = self.get_current_pool_in_state()
                    current_pool = pools[int(user_action) - 1]
                    self.set_current_pool_in_state(current_pool=current_pool)

                self.set_current_state(
                    tag=self.current_state["state_selection"][user_action]
                )
                return self.get_current_state_message()

        # If not transferable state check if it is an action response

        if self.get_current_state_action_responses():
            action_responses = self.get_current_state_action_responses()
            if user_action in list(action_responses.keys()):
                msg = action_responses[user_action]
                return self.return_twilio_formatted_message(msg=msg)

        # If not action reponse, check if action request
        if self.get_current_state_action_requests():
            action_requests = self.get_current_state_action_requests()
            if user_action in list(action_requests.keys()):
                # Need to check if the action request has an input_state
                input_action_states = self.get_current_state_input_action_states()
                if user_action in list(input_action_states.keys()):
                    input_action_states = input_action_states[user_action]
                    self.set_current_state(tag=input_action_states["tag"])
                    msg = input_action_states["message"]
                    return self.return_twilio_formatted_message(msg=msg)

                # Need to check for dynamic state
                if action_requests[user_action] == "/stokvel/my_pools":

                    self.set_current_state(tag="my_pools")
                    return self.get_current_state_message()

                endpoint = action_requests[user_action]
                msg = self.execute_action_request(
                    endpoint=endpoint,
                    payload={
                        "user_number": self.user_number,
                        "current_pool": self.get_current_pool_selection(),
                    },
                )
                return self.return_twilio_formatted_message(msg=msg)

        if (
            isinstance(self.current_state_tag, str)
            and "input_request" in self.current_state_tag
        ):
            endpoint_action = self.current_state["action"]
            self.set_previous_state()
            action_requests = self.get_current_state_action_requests()
            endpoint = action_requests[endpoint_action]
            msg = self.execute_action_request(
                endpoint=endpoint,
                payload={
                    "user_input": user_input,
                    "user_number": self.user_number,
                    "current_pool": self.get_current_pool_selection(),
                },
            )
            return self.return_twilio_formatted_message(msg=msg)

    def execute_action_request(
        self, endpoint: str, payload: Optional[Dict] = None
    ) -> Union[str, Dict]:
        msg = query_endpoint(endpoint_suffix=endpoint, payload=payload)
        return msg

    def get_current_pool_in_state(self):

        return self.current_state.get("current_pool", [])

    def get_current_pool_selection(self):
        return get_current_pool_selection(from_number=self.user_number)

    def set_current_pool_in_state(self, current_pool: str):
        set_current_pool_selection(
            from_number=self.user_number, current_pool=current_pool
        )

    def get_current_state_message(self):
        msg = self.current_state["message"]
        return send_conversational_message(msg)

    def _get_current_state_message_formatted(self):
        message = self.current_state["message"].split(":")[1]
        return message

    def set_current_state(self, tag: str) -> None:
        # Need to set current state in the db
        update_current_state(from_number=self.user_number, current_state_tag=tag)
        self.update_local_states()

    def set_previous_state(self):
        pop_previous_state(from_number=self.user_number)
        self.update_local_states()

    def get_unrecognized_state_response(self):
        if self.current_state:
            msg = self.unrecognized_state + self._get_current_state_message_formatted()
            return send_conversational_message(msg)

        msg = "Sorry, I don't understand. Please activate the service by sending 'Hi' or 'Hello'"
        return send_conversational_message(msg)

    def get_current_state_valid_actions(self) -> List[str]:
        return self.current_state.get("valid_actions", [])

    def get_current_state_action_responses(self) -> Optional[Dict]:
        return self.current_state.get("action_responses", {})

    def get_current_state_action_requests(self) -> Optional[Dict]:
        return self.current_state.get("action_requests", {})

    def get_current_state_input_action_states(self) -> Optional[Dict]:
        return self.current_state.get("input_request_states", {})

    def get_current_state_state_selections(self) -> Optional[Dict]:
        return self.current_state.get("state_selection", {})

    def get_state_tags(self) -> Optional[str]:
        return get_state_responses(from_number=self.user_number)

    def return_twilio_formatted_message(self, msg: str) -> str:
        return send_conversational_message(msg)

    def update_local_states(self) -> None:
        self.current_state_tag = self.get_state_tags()

        # Need to account for dynamic state - Dynamic state will be set within the state manager
        if self.current_state_tag != "my_pools":
            # Initialize to an empty dictionary in case no state is found
            retrieved_state = {}  # type: ignore

            if self.current_state_tag is not None and ":" in self.current_state_tag:
                sub_state_split = self.current_state_tag.split(":")
                inital_state = MESSAGE_STATES  # Start with the base state dictionary

                # Traverse through each sub-state to reach the most nested one
                for state_tag in sub_state_split:
                    retrieved_state = inital_state.get(state_tag, {})  # type: ignore
                    if not retrieved_state:
                        break  # Exit if a sub-state doesn't exist
                    inital_state = retrieved_state  # Move deeper into the state
            else:
                # Handle the case where there are no sub-states
                retrieved_state = MESSAGE_STATES.get(self.current_state_tag, {})  # type: ignore

            # Set the current state based on whether the retrieval was successful
            self.current_state = (
                cast(StateSchema, retrieved_state) if retrieved_state else {}
            )
        else:
            retrieved_state = self.execute_action_request(  # type: ignore
                endpoint="/stokvel/my_pools",
                payload={"user_number": self.user_number},
            )
            self.current_state = json.loads(retrieved_state) if retrieved_state else {}  # type: ignore

    def handle_input_state_validation(
        self, user_input: str
    ) -> Tuple[bool, Union[Optional[float], Optional[int], Optional[str]]]:
        valid_type = self.current_state.get("valid_type")
        try:
            if valid_type == float:
                converted_input = float(user_input)
            elif valid_type == int:
                converted_input = int(user_input)
            elif valid_type == str:
                converted_input = str(user_input)  # type: ignore
            else:
                raise ValueError("Unsupported input type.")
            return True, converted_input
        except ValueError:
            return False, None
