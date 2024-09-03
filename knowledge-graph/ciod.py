import json

from neomodel import (StructuredNode, StringProperty, StructuredRel, RelationshipTo)

class Ciod:

    def __init__(self, id, name, description, linkToStandard):
        self.id = id
        self.name = name
        self.description = description
        self.linkToStandard = linkToStandard

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id
    
    def __str__(self):
        return f"CIOD_NAME: {self.name}\nCIOD_ID: {self.id}\nCIOD_DESCRIPTION: {self.description}"

    @classmethod
    def from_json(cls, json_data):
        return cls(
            json_data["id"],
            json_data["name"],
            json_data["description"],
            json_data["linkToStandard"]
        )
    
    def to_neo4j(self):
        
        ciod_neo4j = Ciod_NEO4J(
            uid=self.id, 
            name=self.name,
            description=self.description,
            linkToStandard=self.linkToStandard
            )
    
        return ciod_neo4j
    
class IncludesRel(StructuredRel):
    usage = StringProperty()
    conditionalStatement = StringProperty()
    informationEntity = StringProperty()

class Ciod_NEO4J(StructuredNode):
    uid = StringProperty(required=True, unique_index=True)
    name = StringProperty(required=True)
    description = StringProperty(required=True)
    linkToStandard = StringProperty(required=True)

    # CIOD to Module relationship
    includes = RelationshipTo(cls_name="module.Module_NEO4J", relation_type="INCLUDES", model=IncludesRel)