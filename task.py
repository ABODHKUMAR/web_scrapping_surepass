
import re
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

# Function to get the captcha image URL
def get_captcha_url(session, response):
    soup = BeautifulSoup(response.content, 'html.parser')
    captcha_img_tag = soup.find('img', {'id': 'form_rcdl:j_idt31:j_idt36'})
    if captcha_img_tag:
        captcha_src = captcha_img_tag.get('src')
        captcha_url = f"https://parivahan.gov.in{captcha_src}"
        print(captcha_url)
        return captcha_url
    else:
        print("Failed to find captcha image tag.")
        return None

# Function to get the captcha image
def get_captcha_image(session, response):
    captcha_url = get_captcha_url(session, response)
    if captcha_url:
        response = session.get(captcha_url)
        captcha_image = Image.open(BytesIO(response.content))
        captcha_image.show()
        return captcha_image
    else:
        print("Failed to fetch captcha image URL.")
        return None

def main():
    
    with requests.Session() as s:
        # Make initial GET request
        r1 = s.get('https://parivahan.gov.in/rcdlstatus/?pur_cd=101')

        # Check if the response is successful
        if r1.status_code == 200:
            print("Verification successful!------>   get_request")
        else:
            print("Verification failed.")
            return
        
        # Get captcha image
        captcha_image = get_captcha_image(s, r1)
        if captcha_image:
            captcha = input("Enter Captcha Code from the image: ").strip()
        else:
            print("Exiting due to captcha image fetch failure.")
            return

        soup1 = BeautifulSoup(r1.content, 'html.parser')
      
        # Extracting jsessionid using regular expressions
        session_id_match = re.search(r'jsessionid=([0-9A-F]+)', r1.text)
        
        if session_id_match:
            session_id = session_id_match.group(1)
            print(session_id_match)
        else:
            print("Failed to extract session ID.")
            return

        # Extracting javax.faces.ViewState
        view_state = soup1.find('input', {'id': 'j_id1:javax.faces.ViewState:0'})
        if view_state:
            view_state = view_state['value']
        else:
            print("Failed to extract view state.")
            return

        payload = {
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": "form_rcdl:j_idt41",
            "javax.faces.partial.execute": "@all",
            "javax.faces.partial.render": "form_rcdl:pnl_show form_rcdl:pg_show form_rcdl:rcdl_pnl",
            "form_rcdl:j_idt41": "form_rcdl:j_idt41",
            "form_rcdl": "form_rcdl",
            "form_rcdl:tf_dlNO": "DL-0420110149646",
            "form_rcdl:tf_dob_input": "09-02-1976",
            'form_rcdl:j_idt31:CaptchaID': captcha,  # Changed captcha ID
            'javax.faces.ViewState': view_state
        }

        post_url = f"https://parivahan.gov.in/rcdlstatus/vahan/rcDlHome.xhtml;jsessionid={session_id}"
        # post_url="https://parivahan.gov.in/rcdlstatus/vahan/rcDlHome.xhtml"
        r2 = s.post(post_url, data=payload)

        if r2.status_code == 200:
            print("Verification successful! ------>post-request")
        else:
            print("Verification failed.")
            return

        soup = BeautifulSoup(r2.content, 'html5lib')
        # print(soup.find_all('td'))
        td_tags = soup.find_all('td')
        print("Length",len(td_tags))
        if len(td_tags) == 0:
            print("Getting Dificultity in Fettching Data Try Again")
            return
        
        print(td_tags)
        # Extract data from <td> tags
        data1 = {
            "Current Status": td_tags[1].text.strip(),
            "Holder's Name": td_tags[3].text.strip(),
            "Old / New DL No.": td_tags[5].text.strip(),
            "Source Of Data": td_tags[7].text.strip(),
            "Initial Issue Date": td_tags[9].text.strip(),
            "Initial Issuing Office": td_tags[11].text.strip(),
            
            # "Non-Transport ": {"from" : td_tags[13].text.strip(), "To "  : td_tags[14].text.strip() } ,
            # "Transport ":  {"from" : td_tags[16].text.strip(), "To "  : td_tags[17].text.strip() } ,
            # "Hazardous Valid Till": td_tags[19].text.strip(),
            # "Hill Valid Till": td_tags[21].text.strip(),
            # "COV Category":td_tags[22].text.strip(),
            # "Class OF Vehicle Details":td_tags[23].text.strip(),
            # "COV Issue Date":td_tags[24].text.strip(),     
        }

        i = 12
        k = 0
        data2 ={}
        while td_tags[i].text.strip() != "Non-Transport":
            data2[td_tags[i].text.strip()] = td_tags[i+2].text.strip()
            i = i + 2
            k = k + 2
            
        
        data3 ={
            
            "Non-Transport ": {"from" : td_tags[13+ k].text.strip(), "To "  : td_tags[14 + k].text.strip() } ,
            "Transport ":  {"from" : td_tags[16+k].text.strip(), "To "  : td_tags[17+ k].text.strip() } ,
            "Hazardous Valid Till": td_tags[19+k].text.strip(),
            "Hill Valid Till": td_tags[21+ k].text.strip(), 
        }
        data4={
            "class_of_vehicle_details":[]
        }
        l=21+k+1
        while l < len(td_tags):
            if l < len(td_tags) and l+1 < len(td_tags) and l+2 < len(td_tags):
                
                obj={
                    "cov_category":td_tags[l].text.strip(),
                    "class_of_vehicle":td_tags[l+1].text.strip(),
                    "cov_issue_date" : td_tags[l+2].text.strip()
                }
                
                data4["class_of_vehicle_details"].append(obj)
                
            l = l + 3
        merged_data = {**data1, **data2, **data3 , **data4}
        print(merged_data)

        # for key, value in data1.items():
        #     if isinstance(value, dict):
        #         print(key + ":")
        #         for k, v in value.items():
        #             print(f"  {k}: {v}")
        #     else:
        #         print(f"{key}: {value}")
        # # i = 0 
        # while i < len(td_tags):
        #     print(td_tags[i].text.strip() , end=" ")
        #     i= i + 1
        #     print()
        
        # # Display extracted data
        # for key, value in data.items():
        #     print(f"{key}: {value}")
                
if __name__ == "__main__":
    main()
