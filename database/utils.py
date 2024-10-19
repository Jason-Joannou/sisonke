def extract_whatsapp_number(from_number: str) -> str:
    if ":" in from_number:
        return from_number.split(":", 1)[1].strip()
    return from_number
