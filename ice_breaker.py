from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from third_party.linkedin import scrape_linkedin_profile
def build_chain():
    summary_input = """
        give the information about {information} that includes: 
        1. a short summary, less than 100 words
        2. two interesting facts about {information}
    """
    prompt = PromptTemplate(input_variables=["information"], template=summary_input)
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain

def search_linkedin(name):
    '''
    流程： 1. 给一个名字通过agent找到linkedin的url 2. 爬取linkedin的信息， 3. 通过chain生成summary
    :return:
    '''
    linkedin_profile_url = linkedin_lookup_agent(name=name)
    summary_template = """
        give the information {information} about a persion from I want you to create: 
        1. a short summary, less than 100 words
        2. two interesting facts about them
    """
    prompt = PromptTemplate(input_variables=["information"], template=summary_template)

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    chain = LLMChain(llm=llm, prompt=prompt)

    linkedin_data = scrape_linkedin_profile(linkedin_profile_url)

    res = chain.run(information=linkedin_data)
    return res

if __name__ == "__main__":
    load_dotenv()  # This loads the .env file into the environment
    # chain = build_chain()
    # res = chain.run(information="the moon")
    # print(res)
    res = search_linkedin("Eden Marco")
    print(res)
