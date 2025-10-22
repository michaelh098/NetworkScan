from py2neo import Graph, Node, Relationship
import json

graph = Graph("bolt://localhost:7687", auth=("neo4j", "testpassword"))

tactic_order = [
    "Reconnaissance",
    "Resource Development",
    "Initial Access",
    "Execution",
    "Persistence",
    "Privilege Escalation",
    "Defense Evasion",
    "Credential Access",
    "Discovery",
    "Lateral Movement",
    "Collection",
    "Command and Control",
    "Exfiltration",
    "Impact"
]


for i in range(len(tactic_order) - 1):
    graph.run(f"""
        MATCH (a:Tactic {{name: '{tactic_order[i]}'}}), (b:Tactic {{name: '{tactic_order[i+1]}'}})
        MERGE (a)-[:NEXT_PHASE]->(b)
    """)
