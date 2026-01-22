import os
import re
from pathlib import Path

SOURCE_DIR = r"c:\Users\Pablo\Desktop\din2\PresentacionDINJDK8_V1\src\cl\aduana\xml\esquemas"
OUTPUT_DIR = r"c:\Users\Pablo\Desktop\din2\litestar_din\src\models"

# Type mapping
TYPE_MAP = {
    "String": "str",
    "BigDecimal": "float",
    "BigInteger": "int",
    "Integer": "int",
    "Long": "int",
    "Double": "float",
    "Boolean": "bool",
    "boolean": "bool",
    "int": "int",
    "long": "int",
    "double": "float",
    "XMLGregorianCalendar": "str", # Simplified for now
    "Date": "str"
}

def parse_java_file(file_path):
    with open(file_path, 'r', encoding='latin-1') as f: # Legacy encoding likely
        content = f.read()

    # Extract package
    pkg_match = re.search(r'package\s+([\w.]+);', content)
    package = pkg_match.group(1) if pkg_match else ""

    # Extract class
    class_match = re.search(r'public\s+class\s+(\w+)', content)
    if not class_match:
        return None
    class_name = class_match.group(1)
    
    # Extract fields
    # Look for @XmlElement followed by variable declaration
    # This regex is approximate
    fields = []
    
    # Split by lines to process annotations usually above fields
    lines = content.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        xml_name = None
        required = False
        
        if line.startswith("@XmlElement"):
            # Extract name
            name_match = re.search(r'name\s*=\s*"([^"]+)"', line)
            if name_match:
                xml_name = name_match.group(1)
            if "required = true" in line:
                required = True
            
            # Look ahead for the field
            j = i + 1
            while j < len(lines):
                next_line = lines[j].strip()
                if next_line.startswith("protected") or next_line.startswith("private"):
                    # protected String secuencia;
                    # protected List<Item> item;
                    field_match = re.search(r'(?:protected|private)\s+([\w<>]+)\s+(\w+);', next_line)
                    if field_match:
                        java_type = field_match.group(1)
                        field_name = field_match.group(2)
                        
                        # Handle List
                        is_list = False
                        if java_type.startswith("List<"):
                            is_list = True
                            inner_type = re.search(r'List<(\w+)>', java_type).group(1)
                            py_type = TYPE_MAP.get(inner_type, inner_type)
                        else:
                            py_type = TYPE_MAP.get(java_type, java_type)
                        
                        fields.append({
                            "xml_name": xml_name,
                            "py_name": field_name,
                            "type": py_type,
                            "list": is_list,
                            "required": required
                        })
                    i = j # Advance outer loop
                    break
                j += 1
        i += 1
        
    return {
        "package": package,
        "class_name": class_name,
        "fields": fields
    }


def collect_models(source_dir):
    models = []
    files = list(Path(source_dir).rglob("*.java"))
    print(f"Found {len(files)} Java files.")
    
    for file_path in files:
        if file_path.name == "ObjectFactory.java" or file_path.name == "package-info.java":
            continue
            
        try:
            model = parse_java_file(file_path)
            if model:
                models.append(model)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    return models

def generate_single_file(models, output_path):
    code = "from pydantic import BaseModel, Field\n"
    code += "from typing import List, Optional\n"
    code += "from pydantic_xml import BaseXmlModel, element, attr\n\n"
    
    # Sort models by name to be deterministic
    models.sort(key=lambda x: x["class_name"])
    
    for model in models:
        class_name = model["class_name"]
        fields = model["fields"]
        
        code += f"class {class_name}(BaseXmlModel):\n"
        # Optional: Add XML tag configuration if class name differs from tag
        # regex for class name usually matches tag in this project
        
        if not fields:
            code += "    pass\n\n"
            continue
        
        for field in fields:
            xml_name = field["xml_name"]
            py_name = field["py_name"]
            py_type = field["type"]
            is_list = field["list"]
            required = field["required"]
            
            # Resolve type forward ref
            if py_type not in TYPE_MAP.values():
                 py_type = f"'{py_type}'"
            
            if is_list:
                type_anot = f"List[{py_type}]"
                default = "default_factory=list"
            else:
                type_anot = py_type if required else f"Optional[{py_type}]"
                default = "default=..." if required else "default=None"
                
            code += f"    {py_name}: {type_anot} = element(tag='{xml_name}', {default})\n"
        code += "\n"

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(code)

def main():
    models = collect_models(SOURCE_DIR)
    # Output to a single file
    output_file = Path(OUTPUT_DIR) / "models.py"
    generate_single_file(models, output_file)
    print(f"Generated {len(models)} models in {output_file}")

if __name__ == "__main__":
    main()

