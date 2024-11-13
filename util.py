import json

    
def txt_to_json(file_path, output_file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        if len(lines) < 2:
            raise ValueError("The text file must contain at least two lines (a title and content).")
        title = lines[0].strip()
        content = "".join(lines[1:]).strip()
        result = {
            "title": title,
            "content": content
        }
        json_result = json.dumps(result, indent=4)
        
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(json_result)
