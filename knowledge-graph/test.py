import os
import json 
from dotenv import load_dotenv
from neo4j import GraphDatabase
from neomodel import config, install_all_labels

# NEO4J Database credentials
load_dotenv()
NEO4J_URL = os.getenv("NEO4J_URL")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

config.DRIVER = GraphDatabase().driver(NEO4J_URL, auth=(NEO4J_USER, NEO4J_PASSWORD))

from neomodel import StructuredNode, StringProperty, UniqueIdProperty

class Person(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True)
    email = StringProperty(unique_index=True)

new_person = Person(name="John Doe", email="john.doe@example.com").save()

