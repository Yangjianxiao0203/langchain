
'''
tools 是langchain要送入Tool中的函数，像是一个具体的action
每次llm都会跑对应的Tool，如果找不到结果，他会更改进来的参数，再跑一次，直到找到结果
'''
from langchain.serpapi import SerpAPIWrapper
from dotenv import load_dotenv

def get_profile_url(text:str) -> str:
    '''
    :Description: 通过输入的名字，返回对应的linkedin profile url
    :return:
    '''
    search_engine = SerpAPIWrapper()
    res = search_engine.run(query=f"{text}")

    return res

if __name__ == "__main__":
    load_dotenv('../.env')
    res = get_profile_url("Jianxiao Yang")
    print(res)