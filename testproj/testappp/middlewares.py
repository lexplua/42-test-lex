from testproj.testappp.models import RequestModel


class HttpLogMiddleware:

    def process_response(self, request, response):
        data = [
            request.method,
            request.get_host() + request.path,
            response.status_code.__str__()
        ]
        record = RequestModel(body=" ".join(data))
        record.save()
        return response
