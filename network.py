from py2neo import Graph, Node, Relationship
import json

# Connect to Neo4j (adjust credentials)
with open("cred.json") as file:
    creds = json.load(file)

# Connect to Neo4j
graph = Graph("bolt://localhost:7687", auth=(creds["username"], creds["password"]))
# Create nodes
isp = Node("Device", name="ISP", brand="Comcast Xfinity")
router = Node("Device", name="Router/Firewall", brand="Cisco")
switch = Node("Device", name="Switch", brand="Cisco")
pc1 = Node("Device", name="PC1", brand="Dell")
pc2 = Node("Device", name="PC2", brand="Lenovo")
printer = Node("Device", name="Printer", brand="HP")
file_server = Node("Device", name="File Server", brand="Dell PowerEdge")
email_server = Node("Device", name="Email Server", brand="Microsoft Exchange")

# Create relationships
graph.create(Relationship(isp, "CONNECTS_TO", router))
graph.create(Relationship(router, "CONNECTS_TO", switch))
graph.create(Relationship(switch, "CONNECTS_TO", pc1))
graph.create(Relationship(switch, "CONNECTS_TO", pc2))
graph.create(Relationship(switch, "CONNECTS_TO", printer))
graph.create(Relationship(switch, "CONNECTS_TO", file_server))
graph.create(Relationship(switch, "CONNECTS_TO", email_server))
