

class ErrorResponse():

    INVALID_PAYLOAD = [
        {
            "response_code": "INVALID_PAYLOAD",
            "response_title": "Request could not be processed. The payload sent is invalid."
        }, 
        420
    ]
    
    INVALID_PARAMETER = [
        {
            "response_code": "INVALID_PAYLOAD",
            "response_title": "Request could not be processed. The Parameter `page` not found"
        }, 
        420
    ]

    INVALID_HEADER = [
        {
        "response_code": "INVALID_HEADER",
        "response_title": "Request could not be processed. The header sent is invalid."
        }, 
        400
    ]

    DUPLICATE_ID = [
        {
        "response_code": "DUPLICATE_ID",
        "response_title": "Request could not be processed. Some id already in use",
    }, 
        420
    ]

    UNAUTHORIZE_ACCESS = [
        {
        "response_code": "UNAUTHORIZE_ACCESS",
        "response_title": "Request could not be processed. invalid Authorization"
    }, 
        420
    ]

    USER_NOT_FOUND = [{
        "response_code": "USER_NOT_FOUND",
        "response_title": "Request could not be processed. User not found!"
    }, 420]

    FAILED_DELETE_USER = [{
        "response_code": "FAILED_DELETE_USER",
        "response_title": "failed to delete user"
    }, 420]

    GENERAL_ERROR_REQUEST = [{
        "response_code": "GENERAL_ERROR_REQUEST",
        "response_title": "Request could not be processed. try again later"
    }, 420]
    
    FAILED_TO_FETCH_DATA = [
        {
        "response_code": "FAILED_TO_FETCH_DATA",
        "response_title": "Request could not be processed. try again later"
    }, 420]

    NO_DATA_TO_FETCH = [
        {
        "response_code": "NO_DATA_TO_FETCH",
        "response_title": "Request could not be processed. try again later"
    }, 200]