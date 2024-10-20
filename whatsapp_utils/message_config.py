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

CLAIM_INSURANCE = {
    "tag": "claim_services",
    "message": """
    Are you are sure you want to claim your unemployment insurance? This will initiate the claims process:
    1. Claim Insurance
    2. Back
    """,
    "valid_actions": ["1", "2"],
    "action_requests": {"1": "/insurance/claim_insurance"},
    "state_selection": {"2": "back_state"},
    "state": 1,
}


EMPLOYER_STATE = {
    "tag": "employer_state",
    "message": """
    Thank you for your response. We will let your employer know of the outcome.
    """,
    "valid_actions": ["1", "2"],
    "action_requests": {"1": "/insurance/process_claim"},
    "state_selection": {"2": "/insurance/claim_revoke"},
}
