import json

with open("notion_response.json", "r", encoding="utf-8") as f:
    data = json.load(f)

record_map = data.get("recordMap", {})
blocks = record_map.get("block", {})

for b_id, b_data in blocks.items():
    val = b_data.get("value", {}).get("value", {})
    if not val:
        val = b_data.get("value", {})
    if not val:
        continue
    
    # Obtener el texto del bloque
    title_prop = val.get("properties", {}).get("title", [])
    text = ""
    for item in title_prop:
        if isinstance(item, list) and len(item) > 0:
            text += item[0]
            
    if "Jóvenes" in text:
        print(f"=== BLOQUE ENCONTRADO: {b_id} ===")
        print(json.dumps(val, indent=2, ensure_ascii=False))
        
        # Si tiene un parent_id o content, imprimir sus detalles
        parent_id = val.get("parent_id")
        print(f"Parent ID: {parent_id}")
        parent_block = blocks.get(parent_id, {}).get("value", {}).get("value", {})
        if parent_block:
            print(f"Parent Type: {parent_block.get('type')}")
            print(f"Parent Title: {parent_block.get('properties', {}).get('title')}")
            
        print("Hijos en content:", val.get("content", []))
