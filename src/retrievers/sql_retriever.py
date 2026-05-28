from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
import duckdb

def query_sql(question: str) -> str:
    # Load the database
    df = duckdb.sql("SELECT * FROM 'data/structured/customers.csv'").df()
    duckdb.sql("CREATE OR REPLACE TABLE customers AS SELECT * FROM df")

    db = SQLDatabase.from_uri("duckdb:///:memory:")
    llm = ChatOpenAI(model="gpt-3.5-turbo")  # or "gpt-4" if you have access
    chain = create_sql_query_chain(llm, db)

    return chain.invoke({"question": question})

import duckdb
from langchain_community.utilities.sql_database import SQLDatabase

# Load CSV into DuckDB
conn = duckdb.connect(database=":memory:")
conn.execute("CREATE TABLE customers AS SELECT * FROM read_csv_auto('data/structured/customers.csv');")

# LangChain-compatible SQL wrapper
db = SQLDatabase.from_uri("duckdb:///:memory:")

# Mock LLM to simulate SQL generation
class MockLLM:
    def invoke(self, inputs):
        print(f"🧠 Mock LLM received: {inputs['question']}")
        return "SELECT COUNT(*) FROM customers;"

llm = MockLLM()
question = "How many customers are there?"
query = llm.invoke({"question": question})
print(f"\n📝 SQL Generated:\n{query}")
print(f"\n📊 Result:\n{conn.execute(query).fetchall()}")
