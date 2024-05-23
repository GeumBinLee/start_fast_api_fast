import datetime
import socket

from fastapi.responses import JSONResponse


class ReturnHandler(Exception):
    def __init__(
        self,
        error=None,
        start_time=None,
        query=None,
        params=None,
        status_code=None,
        message=None,
        result=None,
        client_name=socket.gethostname(),
        client_ip=socket.gethostbyname(socket.gethostname()),
    ):
        self.status_code = status_code or 500
        self.message = message
        self.result = result
        self.start_time = start_time
        self.query = query
        self.params = params
        self.error = error
        self.client_name = client_name
        self.client_ip = client_ip

    def handle_success(self, request=None, dblogger=None):
        msg = (
            f"\nURL: {request.url}\n"
            f"client_name: {self.client_name}\n"
            f"client_ip: {self.client_ip}\n"
            f"status_code: {self.status_code}\n"
        )
        dblogger.info(msg)
        content = {"status_code": self.status_code, "message": self.message}

        if self.result:
            content["result"] = self.result

        try:
            return JSONResponse(
                status_code=self.status_code,
                content=content,
            )
        except TypeError:
            result = []
            for value in self.result:
                item = {}
                for k, v in value.items():
                    if isinstance(v, datetime.date):
                        item[k] = (
                            v.strftime("%Y-%m-%d %H:%M:%S")
                            if isinstance(v, datetime.datetime)
                            else v.strftime("%Y-%m-%d")
                        )
                    else:
                        item[k] = v
                result.append(item)
            content["result"] = result
            return JSONResponse(status_code=self.status_code, content=content)
