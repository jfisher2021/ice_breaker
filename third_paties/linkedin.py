import os 
from dotenv import load_dotenv
import requests
load_dotenv()

def scrape_linkedin_profile(linkedin_profile_url: str, mock:bool= True):
    """Scrape a LinkedIn profile """

    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/jfisher2021/9b60fa11526d6272dddd6d1c362f3c9e/raw/267a7f1d40556af45957ec72e582951bae9cf322/gistfile1.json"
        response = requests.get(linkedin_profile_url, timeout=10)
        data = response.json().get("person") 
    else:
         
        api_endpoint = "https://api.scrapin.io/v1/enrichment/profile"
        params = {
            "apikey": os.environ["SCRAPIN_API_KEY"],
            "linkedInUrl": linkedin_profile_url,
        }

        response = requests.get(
            api_endpoint,
            params=params,
            timeout=10,
        )
        data = response.json().get("person")                       
        
        data = {
            k: v
            for k, v in data.items()
            if v not in ([], "", "", None)
            and k not in ["certifications"]
        }

    return data

if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/jfisherr/"
        )
    )
