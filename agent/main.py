from langgraph.graph import StateGraph,END
from langchain_core.agents import AgentAction,AgentFinish
from langchain_core.messages import AnyMessage,HumanMessage,AIMessage
from typing import TypedDict,Annotated,List,Union
import json
from langchain.chat_models import init_chat_model
from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
import pandas as pd
import operator
load_dotenv()
llm=init_chat_model(model="mistral-small-2506")
def execute_query(df:pd.DataFrame,sql:str)->Union[pd.DataFrame,str]:
	"""Safely execute SQL on DuckDB using the DataFrame"""
	import duckdb
	try:
		result=duckdb.query_df(df,"data",sql).df()
		return result
	except Exception as e:
		return f"Error executing query:{str(e)}"
class AnalystState(TypedDict):
	messages:Annotated[List[AnyMessage],operator.add]
	df:pd.DataFrame
	sql_query:str
	query_result:Union[pd.DataFrame,str,None]
	final_answer:str
def create_analyst_agent():
	llm=ChatMistralAI(model="mistral-small-2506",temperature=0.1)
	def generate_sql(state:AnalystState):
		message=state["messages"]
		df=state['df']
		
		columns=df.columns.tolist()
		dtypes=df.dtypes.astype(str).to_dict()
		schema_info="\n".join([f"-{col}({dtype})" for col,dtype in dtypes.items()])
		
		System_prompt=f"""
		You are precise SQL analyst. Given a pandas DataFrame called 'data', write a DuckDB SQL query to answer the user's quation.
Only return the SQL query,noting else.Do not add explanations.
		Columns in 'data':{schema_info}
		Sample data (first 3  rows):
		{df.head(3).to_dict(orient='records')}
		"""
		enriched_messages=[("system",System_prompt),*[(m.type,m.content) for m in message]]
		response=llm.invoke(enriched_messages)
		sql=response.content.strip()
		return {"messages":[AIMessage(content=sql)],"sql_query":sql}
	def run_query(state:AnalystState):
		sql=state["sql_query"]
		df=state["df"]
		result=execute_query(df,sql)
		return {"query_result":result}
	def finalize_response(state:AnalystState):
		question=state["messages"][0].content
		result=state["query_result"]
		sql=state["sql_query"]
		summary_prompt=f"""
		question:{question}
		SQL:{sql}
		Result:{result}
		Provide a clear,natural language answer. if the results is small, include value. if error,explain simply.
		"""
		response=llm.invoke([("human",summary_prompt)])
		final_answer=response.content
		return {"final_answer":final_answer,"messages":[AIMessage(content=final_answer)]}
	workflow=StateGraph(AnalystState)
	workflow.add_node("generate_sql",generate_sql)
	workflow.add_node("run_query",run_query)
	workflow.add_node("finalize",finalize_response)

	workflow.set_entry_point("generate_sql")
	workflow.add_edge("generate_sql","run_query")
	workflow.add_edge("run_query","finalize")
	workflow.add_edge("finalize",END)

	graph=workflow.compile()
	return graph
		