import xml.etree.ElementTree as ET


def generate_config_xml(classes, aggregations, output_path):
    root_class = next((cls for cls in classes if cls.is_root), None)
    if not root_class:
        raise ValueError("Root class not found")

    # словарь для доступа к классам по именам
    class_dict = {cls.name: cls for cls in classes}

    def add_class_to_xml(parent_element, class_name):
        cls = class_dict.get(class_name)
        if not cls:
            return

        for attr in cls.attributes:
            attr_element = ET.SubElement(parent_element, attr.name)
            attr_element.text = attr.type

        for agg in aggregations:
            if agg.target == cls.name:
                child_class_name = agg.source
                child_class = class_dict.get(child_class_name)

                if child_class:
                    child_element = ET.SubElement(parent_element, child_class.name)
                    if not child_class.attributes and not any(a.target == child_class_name for a in aggregations):
                        child_element.text = " "
                    else:
                        add_class_to_xml(child_element, child_class_name)

    root_element = ET.Element(root_class.name)

    # добавление корневого класса и дочерних элементов
    add_class_to_xml(root_element, root_class.name)

    tree = ET.ElementTree(root_element)
    with open(output_path, "wb") as file:
        tree.write(file, encoding="utf-8", xml_declaration=True, short_empty_elements=False)
