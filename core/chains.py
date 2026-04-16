
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from core.llm_model import model2 as llm


system_prompt_sql = '''
You are a SQLite SQL generator for a resume database.

SCHEMA:
resume_base(resume_id, name, summary)
contact(resume_id, email, phone, linkedin, github, hugging_face, kaggle)
certifications(resume_id, certification_name)
education(resume_id, institution, degree, start_date, end_date)
experience(resume_id, title, company, start_date, end_date)
projects(resume_id, name, description, technologies, url, difficulty_score)

RELATIONS:
resume_base.resume_id = contact.resume_id
resume_base.resume_id = education.resume_id
resume_base.resume_id = experience.resume_id
resume_base.resume_id = projects.resume_id

TASK:
Convert user query → valid SQLite SQL.

OUTPUT RULES:
- One line only
- Only SQL
- No markdown, no backticks, no text

RELEVANCE:
- If not answerable from schema → IRRELEVANT QUERY

QUERY RULES:
- Use COLLATE NOCASE on searches
- Use only listed tables/columns
- Use explicit JOIN when needed
- Always join on resume_id
- No invented schema
'''

primary_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt_sql),
    ("human", "Query: {user_query}")
])

primary_chain = primary_template | llm | RunnableLambda(lambda response: response.content)

def generate_sql_query(user_query):
    return primary_chain.invoke({
        "user_query": user_query
    })



system_prompt_analyst = '''
You are a data analyst.

INPUT:
- User question
- SQL query result (from database)

TASK:
- Generate a clear natural language answer based ONLY on the SQL result
- If result is empty, say no matching data found
- Generate short and concise answer in markdown format
- Do NOT generate SQL
- Do NOT hallucinate missing data
'''


# Secondary Chain
secondary_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt_analyst),
    ("human", "Query: {user_query}\nResults: {db_results}")
])

secondary_chain = secondary_template | llm | RunnableLambda(lambda response: response.content)

def generate_nl_answer(user_query, db_results):
    return secondary_chain.invoke({
        "user_query": user_query,
        "db_results": db_results
    })

 