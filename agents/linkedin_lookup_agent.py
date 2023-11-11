from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

from langchain.agents import initialize_agent, Tool, AgentType

from tools.tools import get_profile_url


def lookup(name: str) -> str:
    '''
    agent 流程： 1. 外界的tool是google serach api，找url的
    大模型的reAct：
    I need to use the linkedin_crawler tool to search for the Linkedin profile of Jianxiao Yang.
    Action: linkedin_crawler
    Action Input: 'Jianxiao Yang'
    Observation: ['Jianxiao Yang. PhD in Biomathematics. University of California, Los Angeles. San Francisco Bay Area. 168 followers 169 connections.', 'University of California, Los Angeles - \u202a\u202aCited by 71\u202c\u202c', 'Forked from OHDSI/Cyclops. Cyclops (Cyclic coordinate descent for logistic, Poisson and survival analysis) is an R package for performing large scale ...', '6 narrowband receiver is proposed, including frame synchronization, timing synchronization, and carrier frequency synchronization. This proposed single-carrier ...', 'Works (22) · Preparation of discarded cigarette butt-derived activated carbon and its decolorization for waste edible oils · Eco-Friendly ...', 'Publications in Journals. •Jianxiao Yang, Benoit Geller, Meng Li, and Tong Zhang, “An Information Theory Perspective for the Binary STT-MRAM Cell Operation ...', 'Jianxiao Yang. Affiliation. Institute of Information & Communication Engineering, University of Zhejiang, Hangzhou, China. Publication Topics. AWGN channels ...', 'List of computer science publications by Jianxiao Yang.', 'Jianxiao Yang is on Facebook. Join Facebook to connect with Jianxiao Yang and others you may know. Facebook gives people the power to share and makes the...']
    Thought:The LinkedIn profile for Jianxiao Yang has been found.
    Final Answer: https://www.linkedin.com/in/jianxiaoyang
    '''
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    template = """given the full name of {name_of_person}, I want you to get it me a link to their Linkedin profile page. Your answer should be only a url. """
    prompt = PromptTemplate(input_variables=["name_of_person"], template=template)

    crawl_tool = Tool(
        name="linkedin_crawler",
        description="This tool crawls linkedin for a given name and returns a url to the profile page",
        func=get_profile_url,
    )
    tools = [crawl_tool] # tools 就像action的一环

    agent = initialize_agent(tools=tools,agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,verbose=True,llm=llm)

    linkedin_url = agent.run(prompt.format_prompt(name_of_person=name))

    print("linkedin url: ", linkedin_url)
    return linkedin_url
