from rest_framework import response

def try_except(func):
    def exe(*args, **kwargs):
        request = args[1]
        try:
            return func(*args, **kwargs)

        except Exception as e:
            output = {
                "message": f"Error while processing {str(request.method)} request",
                "details": str(e)
            }
            return response.Response(output)
    return exe