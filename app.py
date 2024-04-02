import requests
from bs4 import BeautifulSoup

loginurl_post = 'https://the-internet.herokuapp.com/authenticate'
secure_url_get = 'https://the-internet.herokuapp.com/secure'
login_page_url = 'https://the-internet.herokuapp.com/login'
actual_website_link ='https://parivahan.gov.in/rcdlstatus/?pur_cd=101'

url = "https://parivahan.gov.in/rcdlstatus/vahan/rcDlHome.xhtml"
payload = {
    'username': 'tomsmith',
    'password': 'SuperSecretPassword!'
}

with requests.Session() as s:
    s.post(loginurl_post, data=payload)
    r = s.get(secure_url_get)  # Note: Using the same session 's' for subsequent requests
    soup = BeautifulSoup(r.content, 'html.parser')
    print(soup.prettify())



# https://parivahan.gov.in/rcdlstatus/vahan/rcDlHome.xhtml    ----------post request
# https://parivahan.gov.in/rcdlstatus/vahan/rcDlHome.xhtml  
# https://parivahan.gov.in/rcdlstatus/vahan/javax.faces.resource/theme.css?ln=primefaces-parivahan   ----------get request