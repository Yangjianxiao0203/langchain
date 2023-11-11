import os
import requests
import json
from third_party.config import Config
from third_party.utils import save_json_to_file
from dotenv import load_dotenv

Debug = Config["debug"]


def scrape_linkedin_profile(linked_in_url):
    compress_linkedin = Config["compress_linkedin"]
    if Debug:
        response = requests.get(
            "https://gist.githubusercontent.com/Yangjianxiao0203/494f564be636f3ea0884d90d5cd669b3/raw/41e5475cd486d364d5821093d909167c1f500d90/jianxiao-linkedin.json"
        )
        res_json = response.json()
        if compress_linkedin:
            res_json = compress_linkedin_json(res_json)
        return res_json

    try:
        api_key = os.environ["PROXYCURL_API_KEY"]
        if api_key is None:
            raise Exception("PROXYCURL_API_KEY is empty")
    except:
        load_dotenv(dotenv_path="../.env")
        api_key = os.getenv("PROXYCURL_API_KEY")
    headers = {"Authorization": "Bearer " + api_key}
    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
    params = {
        "linkedin_profile_url": linked_in_url,
        "extra": "include",
        "github_profile_id": "include",
        "facebook_profile_id": "include",
        "twitter_profile_id": "include",
        "personal_contact_number": "include",
        "personal_email": "include",
        "inferred_salary": "include",
        "skills": "include",
        "use_cache": "if-present",
        "fallback_to_cache": "on-error",
    }
    response = requests.get(api_endpoint, params=params, headers=headers)
    if response.status_code != 200:
        raise Exception("Error: {}".format(response.text))
    res_json = response.json()
    save_json_to_file(Config["linkedin_json_path"], res_json)
    if compress_linkedin:
        res_json = compress_linkedin_json(res_json)
    return res_json


def compress_linkedin_json(linkedin_json):
    data = {
        k: v
        for k, v in linkedin_json.items()
        if v not in ([], "", " ", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")
    return json.dumps(data, indent=2)


if __name__ == "__main__":
    linked_in_url = "https://www.linkedin.com/in/jianxiaoyang/"
    res = scrape_linkedin_profile(linked_in_url)
    print(res)
