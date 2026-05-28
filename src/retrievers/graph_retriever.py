from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
auth = ("neo4j", "neo4jpass123")  # Update with your actual password

driver = GraphDatabase.driver(uri, auth=auth)

def run_query(tx):
    result = tx.run("MATCH (f:Facility)-[r]->(reg:Regulation) RETURN f.name, type(r), reg.type LIMIT 5")
    for record in result:
        print(f"🏭 {record['f.name']} -[{record['type(r)']}]-> {record['reg.type']}")

with driver.session() as session:
    session.read_transaction(run_query)
def query_graph(query: str = None) -> str:
    """
    Query Neo4j to get facilities and their regulation status.
    Ignores the input query — returns a pre-defined read.
    """
    from neo4j import GraphDatabase
    from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def run_query(tx):
        result = tx.run("""
            MATCH (f:Facility)-[r]->(reg:Regulation)
            RETURN f.name AS facility, type(r) AS relationship, reg.type AS regulation
        """)
        return [
            f"🏭 {row['facility']} -[{row['relationship']}]-> {row['regulation']}"
            for row in result
        ]

    with driver.session() as session:
        output = session.execute_read(run_query)

    driver.close()
    return "\n".join(output)
if __name__ == "__main__":
    print(query_graph())
