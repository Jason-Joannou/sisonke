from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class StateSchema(BaseModel):
    tag: str = Field(..., example="claims_service")
    message: str = Field(..., example="Welcome to our claims services!")
    valid_actions: Optional[List[str]] = Field(..., example=["1", "2", "3"])
    state: int = Field(..., example=1)
    action_responses: Optional[Dict] = Field(
        {},
        example={
            "1": "Please register through our online portal: https://sisonke.com/onboard",
        },
    )
    action_requests: Optional[Dict] = Field({}, examples={"1": "/insurance/claims"})
    state_selection: Optional[Dict] = Field({}, examples={"1": "claims"})
    input_request_states: Optional[Dict[str, Dict]] = Field(
        {},
        examples={
            "1": {
                "tag": "pay_insurance",
                "message": "Please enter the amount you would like to pay",
            }
        },
    )
    current_insurance_pool: Optional[List] = Field(
        [], examples=["MobilePhones", "Vehicles"]
    )
