
import requests

def check_response_code(url):
    """
    Checks the http response code for get() request to a page
    :param url:
    :return: response code after get request sent to url
    """
    
    try:
        page = requests.get(url)        #to extract page from website
        html_code = page.content        #to extract html code from page
        response_code = page.status_code
        print (response_code)
        if (response_code == 400) or (response_code == 401) or (response_code == 402) or (response_code == 403) or (response_code == 405) or (response_code == 406) or (response_code == 407) or (response_code == 408):
            print(response_code)
            return(response_code)
        else:
            return(0)

    except requests.exceptions.Timeout:
        return(1)
                    
    except Exception as e:
            print(e)
            return(1)

