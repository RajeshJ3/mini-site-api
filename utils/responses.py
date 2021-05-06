from drf_yasg2 import openapi

GET_RESPONSES = {
    200: openapi.Response("Successful GET Request"),
    401: openapi.Response("Unauthorized"),
    500: openapi.Response("Internal Server Error")
}

POST_RESPONSES = {
    200: openapi.Response("Successful POST Request"),
    401: openapi.Response("Unauthorized"),
    422: openapi.Response("Unprocessable Entity"),
    500: openapi.Response("Internal Server Error")
}

PUT_RESPONSES = {
    200: openapi.Response("Successful PUT Request"),
    401: openapi.Response("Unauthorized- Authentication credentials were not provided. || Token Missing or Session Expired"),
    422: openapi.Response("Unprocessable Entity"),
    500: openapi.Response("Internal Server Error")
}

DELETE_RESPONSES = {
    200: openapi.Response("Successful DELETE Request"),
    500: openapi.Response("Internal Server Error")
}
