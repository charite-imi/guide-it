from neomodel import (StructuredNode, StringProperty, RelationshipTo)

class Attribute:

    def __init__(self, id, name, tag, keyword, valueRepresentation, valueMultiplicity, retired):
        self.id = id
        self.name = name
        self.tag = tag
        self.keyword = keyword
        self.valueRepresentation = valueRepresentation
        self.valueMultiplicity = valueMultiplicity
        self.retired = retired

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self) -> str:
        return f"Attribute(Name: {self.name}, ID: {self.id}, Tag: {self.tag}, Retired: {self.retired})"

    @classmethod
    def from_json(cls, json_data):
        return cls(
            json_data["id"],
            json_data["name"],
            json_data["tag"],
            json_data["keyword"],
            json_data["valueRepresentation"],
            json_data["valueMultiplicity"],
            json_data["retired"]
        )
    
    def to_neo4j(self):
        
        module_neo4j = Attribute_NEO4J(
            uid = self.id,
            name = self.name,
            tag = self.tag,
            keyword = self.keyword,
            valueRepresentation = self.valueRepresentation,
            valueMultiplicity = self.valueMultiplicity,
            retired = self.retired
            )
    
        return module_neo4j

class Attribute_NEO4J(StructuredNode):
    
    uid = StringProperty(required=True, unique_index=True)
    name = StringProperty(required=True)
    tag = StringProperty(required=True)
    keyword = StringProperty(required=True)
    valueRepresentation = StringProperty(required=True)
    valueMultiplicity = StringProperty(required=True)
    retired = StringProperty(required=True)