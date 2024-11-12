import xml.etree.ElementTree as ET
from typing import List, Optional


# определение классов для демаршаллинга
class Attribute:
    def __init__(self, name: str, type: str):
        self.name = name
        self.type = type


class UMLClass:
    def __init__(self, name: str, is_root: bool, documentation: Optional[str]):
        self.name = name
        self.is_root = is_root
        self.documentation = documentation
        self.attributes: List[Attribute] = []

    def add_attribute(self, attribute: Attribute):
        self.attributes.append(attribute)


class Aggregation:
    def __init__(self, source: str, target: str, source_multiplicity: str, target_multiplicity: str):
        self.source = source
        self.target = target
        self.source_multiplicity = source_multiplicity
        self.target_multiplicity = target_multiplicity


# демаршаллинг
def demarshal_xml(xml_data: str):
    root = ET.fromstring(xml_data)
    classes = []
    aggregations = []

    for cls in root.findall('Class'):
        class_name = cls.get('name')
        is_root = cls.get('isRoot') == 'true'
        documentation = cls.get('documentation')

        uml_class = UMLClass(name=class_name, is_root=is_root, documentation=documentation)

        for attr in cls.findall('Attribute'):
            attribute = Attribute(name=attr.get('name'), type=attr.get('type'))
            uml_class.add_attribute(attribute)

        classes.append(uml_class)

    for agg in root.findall('Aggregation'):
        aggregation = Aggregation(
            source=agg.get('source'),
            target=agg.get('target'),
            source_multiplicity=agg.get('sourceMultiplicity'),
            target_multiplicity=agg.get('targetMultiplicity')
        )
        aggregations.append(aggregation)

    return classes, aggregations


