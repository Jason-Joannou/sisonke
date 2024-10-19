def check_if_number_exists_sqlite(from_number: str) -> bool:
    from_number = extract_whatsapp_number(from_number=from_number)
    query = "SELECT * FROM USERS WHERE user_number = :from_number"
    with sqlite_conn.connect() as conn:
        try:
            cursor = conn.execute(text(query), {"from_number": from_number})
            result = cursor.fetchone()
            if result:
                return True

            return False
        except Exception as e:
            print(f"An error occurred in check_if_number_exists: {e}")
            raise e
