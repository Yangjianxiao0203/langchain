"""
tools 是langchain要送入Tool中的函数，像是一个具体的action
每次llm都会跑对应的Tool，如果找不到结果，他会更改进来的参数，再跑一次，直到找到结果
"""
from langchain.serpapi import SerpAPIWrapper
from dotenv import load_dotenv


def get_profile_url(name,description="") -> str:
    """
    :Description: 通过输入的名字和描述，返回对应的linkedin profile url
    :return:
    """
    text = f"{name} {description} linkedin"
    search_engine = CustomSerpAPIWrapper()
    res = search_engine.run(query=f"{text}")
    return res

class CustomSerpAPIWrapper(SerpAPIWrapper):
    def __init__(self):
        super(CustomSerpAPIWrapper,self).__init__()

    @staticmethod
    def _process_response(res: dict) -> str:
        if "error" in res.keys():
            raise ValueError(f"Got error from SerpAPI: {res['error']}")
        result_str = ""
        for organic_result in res.get("organic_results", []):
            if "snippet" in organic_result:
                result_str += f"Snippet: {organic_result['snippet']}\t"
            if "link" in organic_result:
                result_str += f"Link: {organic_result['link']}\n"

        if len(result_str) > 0:
            return result_str
        else:
            return "No good search result found"



if __name__ == "__main__":
    load_dotenv("../.env")
    res = get_profile_url("Jianxiao Yang",description="He studies in Boston University and has intenship experience in Uber")
    print(res)
