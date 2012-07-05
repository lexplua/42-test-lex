from testproj.testappp.models import RequestModel
class HttpLogMiddleware:

    def process_response(self,request, response):
        record = RequestModel(
                    body = " ".join([request.method,request.get_host()+request.path,response.status_code.__str__()])
                )
        record.save()
        return response