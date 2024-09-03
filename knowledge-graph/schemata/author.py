from pydantic import BaseModel, AnyUrl, field_validator
from typing import Union, List, ClassVar

from neomodel import (StructuredNode, StringProperty, IntegerProperty, UniqueIdProperty, RelationshipTo)

class CIOD:

    def __init__(self, name, id, description, linkToStandard):
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
            json_data["name"],
            json_data["id"],
            json_data["description"],
            json_data["linkToStandard"]
        )
    
class Author(BaseModel):

    AUTHOR_FIELDS: ClassVar[str] = "authorId,externalIds,name,affiliations,paperCount,citationCount,hIndex"
    
    authorId: int = None
    externalIds: dict = {}
    name: str = ""
    affiliations: Union[List[str], None] = []
    paperCount: Union[int, None] = None
    citationCount: Union[int, None] = None
    hIndex: Union[int, None] = None

class Author_NEO4J(StructuredNode):
    
    authorId = IntegerProperty(required=True, unique_index=True)
    name = StringProperty(required=True)
    paperCount = IntegerProperty(required=True)
    citationCount = IntegerProperty(required=True)
    hIndex = IntegerProperty(required=True)