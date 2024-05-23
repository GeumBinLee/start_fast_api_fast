from fastapi import Request


def get_base_url(request: Request):
    """
    요청 객체로부터 기본 URL을 반환합니다.
    :param request: FastAPI 요청 객체
    :return: 기본 URL 문자열
    """
    if request is None:
        return "http://localhost:8000"
    return str(request.base_url)
