from pydantic import BaseModel, AnyUrl, field_validator
from typing import Union, ClassVar, List

from neomodel import (StructuredNode, StringProperty, IntegerProperty, UniqueIdProperty, Relationship, RelationshipTo)

from .author import Author_NEO4J

class Paper(BaseModel):
    
    PAPER_FIELDS: ClassVar[str] = "paperId,corpusId,title,year,authors.authorId,publicationTypes,isOpenAccess,openAccessPdf"

    paperId: str = ""
    corpusId: int = None
    title: str = ""
    authors: Union[List[dict], List[str]] = []
    year: Union[int, None] = None
    publicationTypes: Union[List[str], None] = []
    isOpenAccess: bool = False
    openAccessPdf: Union[AnyUrl, dict, None] = None

    @field_validator("openAccessPdf")
    def openAccessPdf_to_url(cls, value: Union[dict, None]) -> Union[AnyUrl, None]:
        if isinstance(value, dict):
            value = value.get("url")    
        return value
    
    @field_validator("authors")
    def authors_to_str_list(cls, value: Union[List[dict], List[str]]) -> List[str]:
        if isinstance(value[0], dict):
            value_as_str = [author.get("authorId") for author in value]
            # Remove undefined authors
            value_as_str_without_none = [value for value in value_as_str if (value != None)]
        return value_as_str_without_none
        
