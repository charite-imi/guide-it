import os
import json
from dotenv import load_dotenv
from neo4j import GraphDatabase
from neomodel import config, install_all_labels

from ciod import Ciod
from module import Module
from attribute import Attribute

from mapper import CiodToModules, ModuleToAttributes

# NEO4J Database credentials
load_dotenv()
NEO4J_URL = os.getenv("NEO4J_URL")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

config.DRIVER = GraphDatabase().driver(NEO4J_URL, auth=(NEO4J_USER, NEO4J_PASSWORD))

# IMPORTANT: Ensure uniquness!!!
install_all_labels() 
    
ciods_path = 'dicom/ciods.json'
modules_path = 'dicom/modules.json'
attributes_path = 'dicom/attributes.json'

with open(ciods_path, 'r') as file:
    ciods = json.load(file)
with open(attributes_path, 'r') as file:
    attributes = json.load(file)
with open(modules_path, 'r') as file:
    modules = json.load(file)
with open("dicom/module_to_attributes.json", 'r') as file:
    module_to_attributes = json.load(file)

ciods_set = {Ciod.from_json(ciod) for ciod in ciods}
modules_set = {Module.from_json(module) for module in modules}
attributes_set = {Attribute.from_json(attribute) for attribute in attributes}

ciod_modules_mapper = CiodToModules()
modules_attributes_mapper = ModuleToAttributes()
ciod_modules_mapper.map("dicom/ciod_to_modules.json")
modules_attributes_mapper.map("dicom/module_to_attributes.json")

ciod_dict = dict()
for ciod in ciods_set:
    ciod_neo4j = ciod.to_neo4j()
    ciod_dict[ciod.id] = ciod_neo4j
    try:
        ciod_neo4j.save()
    except:
        print(f"[!] CIOD ERROR: {ciod.name} cannot be saved!")

module_dict = dict()
for module in modules_set:
    module_neo4j = module.to_neo4j()
    module_dict[module.id] = module_neo4j
    try:    
        module_neo4j.save()
    except:
        print(f"[!] MODULE ERROR: {module.name} cannot be saved!")

attribute_dict = dict()
for attribute in attributes_set:
    attribute_neo4j = attribute.to_neo4j()
    attribute_dict[attribute.id] = attribute_neo4j
    try:
        attribute_neo4j.save()
    except:
        print(f"[!] ATTRiBUTE ERROR: {attribute.name} cannot be saved!")

for mapping in ciod_modules_mapper.mapping:
    ciod_id, module_id, usage, conditionalStatement, informationEntity = mapping["ciodId"], mapping["moduleId"], mapping["usage"], mapping["conditionalStatement"], mapping["informationEntity"]
    conditionalStatement = str(conditionalStatement)
    try:
        ciod_dict[ciod_id].includes.connect(module_dict[module_id], {"usage": usage, "conditionalStatement": conditionalStatement, "informationEntity": informationEntity})
    except:
        print(f"[!] RELATIONSHIP ERROR: {ciod_id} to {module_id} cannot be saved!")

for mapping in modules_attributes_mapper.mapping:
    module_id, attribute_id, type, linkToStandard, description = mapping["moduleId"], mapping["attributeId"], mapping["type"], mapping["linkToStandard"], mapping["description"]
    try:
        module_dict[module_id].contains.connect(attribute_dict[attribute_id], {"type": type, "linkToStandard": linkToStandard, "description": description})
    except:
        print(f"[!] RELATIONSHIP ERROR: {module_id} to {attribute_id} cannot be saved!")