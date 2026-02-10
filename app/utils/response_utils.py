def success_response(data: any, message: str = "Success"):
    return {"success": True, "message": message, "data": data}

def error_response(message: str, code: int = 400):
    return {"success": False, "message": message, "code": code}
