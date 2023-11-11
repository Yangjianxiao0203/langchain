from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

def build_chain():
    summary_input = """
        give the information about {information} that includes: 
        1. a short summary, less than 100 words
        2. two interesting facts about {information}
    """
    prompt = PromptTemplate(input_variables=["information"], template=summary_input)
    llm = ChatOpenAI(model_name = "gpt-3.5-turbo",temperature=0)
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain

if __name__ =='__main__':
    load_dotenv()  # This loads the .env file into the environment
    chain = build_chain()
    res = chain.run(information="the moon")
    print(res)