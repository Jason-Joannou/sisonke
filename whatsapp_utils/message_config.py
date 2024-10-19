UNREGISTERED_NUMBER = {
    "tag": "unregistered_number",
    "message": """
    Hi there! We noticed this number is not registered with us. Please enter your rafiki wallet address to continue:
    """,
    "action_requests": {
        "1": "/validation/wallet",
    },
}

REGISTERED_NUMBER = {
    "tag": "registered_number",
    "message": """
    Hi there, welcome back! Please select one of the following options to proceed:
        1. Insurance
        2. Claims
        3. Manage
    """,
    "valid_actions": ["1", "2", "3"],
    "state_selection": {
        "1": "insurance_services",
        "2": "claim_services",
        "3": "manage_services",
    },
    "state": 0,
}

INSURANCE_SERVICES = {
    "tag": "insurance_services",
    "message": """
    Please select one of the following options to proceed:
    1. Unemployment insurance
    2. Product Insurance
    3. My Insurance
    4. Back
    """,
    "valid_actions": ["1", "2", "3", "4"],
    "action_responses": {
        "1": "Please apply for unemployment insurance through our online portal: http://localhost:5000/insurance/unemployment",
        "2": "Not for Demo Purposes",
    },
    "action_requests": {"3": "/stokvel/my_stokvels"},
    "state_selection": {"4": "back_state"},
    "state": 1,
}
