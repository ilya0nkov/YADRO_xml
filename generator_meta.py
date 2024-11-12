import json


def generate_meta_json(classes, aggregations, output_path):
    class_dict = {cls.name: cls for cls in classes}
    meta_data = []

    for cls in classes:
        class_data = {
            "class": cls.name,
            "documentation": cls.documentation,
            "isRoot": cls.is_root,
            "parameters": []
        }

        for attr in cls.attributes:
            if attr.name != cls.name:
                class_data["parameters"].append({
                    "name": attr.name,
                    "type": attr.type
                })

        for aggregation in aggregations:
            # агрегация для получения min/max
            if aggregation.source == cls.name:
                # пропуск min и max для BTS
                if cls.name == "BTS":
                    continue

                if ".." in aggregation.source_multiplicity:
                    min_value, max_value = aggregation.source_multiplicity.split("..")
                    class_data["min"] = min_value
                    class_data["max"] = max_value
                else:
                    class_data["min"] = aggregation.source_multiplicity
                    class_data["max"] = aggregation.source_multiplicity
            # агрегация для получения parameters
            elif aggregation.target == cls.name:
                child_class = class_dict.get(aggregation.source)
                if child_class:
                    class_data["parameters"].append({
                        "name": child_class.name,
                        "type": "class"
                    })

        meta_data.append(class_data)

    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(meta_data, json_file, indent=4, ensure_ascii=False)

