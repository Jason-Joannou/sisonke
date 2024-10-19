UNREGISTERED_NUMBER = {
    "tag": "unregistered_number",
    "message": """
    Hi there! We noticed this number is not registered with us. Please enter your rafiki wallet address to continue:
    """,
    "action_requests": {
        "1": "/test_endpoint",
    },
    "input_request_states": {
        "1": {
            "tag": "unregistered_number:input_request_states:1",
            "message": "Please enter your rafiki wallet address",
            "valid_type": str,
            "invalid_message": "Please make ensure your new name is at least one character long. Returning to previous menu.",
            "action": "1",
        },
    },
}
