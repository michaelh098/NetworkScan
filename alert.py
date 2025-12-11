from py2neo import Graph, Node, Relationship
import json

with open("cred.json") as file:
    creds = json.load(file)

with open("threat_db.json",'r') as file:
    threats = json.load(file)

graph = Graph("bolt://localhost:7687", auth=(creds["username"], creds["password"]))

for threat in threats:
    if not (threat["Mitre Techniques"] or threat["Mitre Tactics"] or threat["relevant_devices"]):
        continue

    # Use link as a unique identifier for the Alert
    alert = Node("Alert",
        title=threat.get("Alert"),
        link=threat["link"],
        Mitigation=threat["Mitigation Suggestions"]
    )
    graph.merge(alert, "Alert", "link")   # merge by unique property

    # Connect to tactics
    for t in threat["Mitre Tactics"]:
        tactic = graph.nodes.match("Tactic", name=t).first()
        if tactic:
            graph.merge(Relationship(alert, "RELATED_TACTIC", tactic))

    # Connect to techniques
    for code in threat["Mitre Techniques"]:
        tech = graph.nodes.match("Technique", external_id=code).first()
        if tech:
            graph.merge(Relationship(alert, "RELATED_TECHNIQUE", tech))

    # Connect to devices
    for dev in threat["relevant_devices"]:
        matches = graph.nodes.match("Device").where(f"_.name CONTAINS '{dev}'")
        for device in matches:
            graph.merge(Relationship(alert, "TARGETS", device))
