import streamlit as st
import pandas as pd

from agent.main import create_analyst_agent
import util.file_processor as fp
from langchain_core.messages import HumanMessage
st.set_page_config(page_title="Data analyst",layout="wide")
st.title("Chat withdata")
uploaded_file=st.file_uploader("Upload CSV or EXCEL",type=["csv","xlsx"])

if uploaded_file:
	with st.spinner("Processing file...<>"):
		temp_path,col,df=fp.preprocess_and_save(uploaded_file)
		if df is not None:
			st.session_state.df = df
			st.session_state.columns = col
			st.session_state.uploaded_file_name = uploaded_file.name
			st.success("File loaded!")
	st.subheader("Data Preview")
	st.dataframe(st.session_state.df.head(10))
	
	if "graph" not in st.session_state:
		with st.spinner(f"Initializing agent"):
			st.session_state.graph=create_analyst_agent()
	user_query=st.text_area("question",height=120)
	if st.button("Run analysis"):
		if not user_query.strip():
			st.warning("Please enter a question")
		else:
			with st.spinner("Thinking with Mistral...<>"):
				try:
					inputs={
						"messages":[HumanMessage(content=user_query)],
						"df":st.session_state.df
					}
					result=st.session_state.graph.invoke(inputs,{"recursion_limit":10})
					st.markdown("Final Answer")
					st.markdown(result["final_answer"])
					st.markdown("Generated SQL")


					st.code(result["sql_query"],language="sql")
					st.markdown("Result")
					res=result["query_result"]
					if isinstance(res,pd.DataFrame):
						st.dataframe(res)
					else:
						st.markdown(f"`{res}`")
				except Exception as e:
					st.error(f"Error:{str(e)}")
					st.exception(e)