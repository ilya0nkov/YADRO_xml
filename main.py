import os
from generator_config import generate_config_xml
from generator_meta import generate_meta_json
from input_data_parser import demarshal_xml


def main():
    input_file = "impulse_test_input.xml"
    output_dir = "out"
    config_file = os.path.join(output_dir, "config.xml")
    meta_file = os.path.join(output_dir, "meta.json")

    if not os.path.exists(input_file):
        print(f"Error: file '{input_file}' not found")
        return

    os.makedirs(output_dir, exist_ok=True)
    print(f"The directory '{output_dir}' created/exists")

    with open(input_file, "r") as file:
        xml_data = file.read()

    classes, aggregations = demarshal_xml(xml_data)

    generate_config_xml(classes, aggregations, config_file)
    print(f"The file '{config_file}' created/owerwritten")

    generate_meta_json(classes, aggregations, meta_file)
    print(f"The file '{meta_file}' created/owerwritten")


if __name__ == "__main__":
    main()
