from fastapi import Request


def get_base_url(request: Request):
    if request is None:
        return f"http://localhost:8000"
    return request.base_url
