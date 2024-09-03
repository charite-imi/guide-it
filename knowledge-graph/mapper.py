import json

class ModuleToAttributes:

    def __init__(self):
        self.mapping = None
        
    def map(self, mapping_file):
        with open(mapping_file, 'r') as file:
            self.mapping = json.load(file)

        for mapping in self.mapping:
            mapping["attributeId"] = self.get_attribute_id_from_tag(mapping["tag"])
            
    def get_attribute_id_from_tag(self, tag):
        attribute_id = tag.replace("(", "").replace(")", "").replace(",", "").lower()
        return attribute_id
    
class CiodToModules:

    def __init__(self):
        self.mapping = None
        
    def map(self, mapping_file):
        with open(mapping_file, 'r') as file:
            self.mapping = json.load(file)