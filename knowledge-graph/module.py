import json

from neomodel import (StructuredNode, StringProperty, StructuredRel, RelationshipTo)

class Module:

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
        return f"MODULE_NAME: {self.name}\nMODULE_ID: {self.id}\nMODULE_DESCRIPTION: {self.description}"

    @classmethod
    def from_json(cls, json_data):
        return cls(
            json_data["id"],
            json_data["name"],
            json_data["description"],
            json_data["linkToStandard"]
        )
    
    def to_neo4j(self):
        
        module_neo4j = Module_NEO4J(
            uid=self.id, 
            name=self.name,
            description=self.description,
            linkToStandard=self.linkToStandard
            )
    
        return module_neo4j
    
class ContainsRel(StructuredRel):
    type = StringProperty()
    linkToStandard = StringProperty()
    description = StringProperty()
    
class Module_NEO4J(StructuredNode):
    
    uid = StringProperty(required=True, unique_index=True)
    name = StringProperty(required=True)
    description = StringProperty(required=True)
    linkToStandard = StringProperty(required=True)

    # Module to attribute relationship
    contains = RelationshipTo(cls_name="attribute.Attribute_NEO4J", relation_type="CONTAINS", model=ContainsRel)