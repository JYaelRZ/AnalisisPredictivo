import json

with open("notion_response.json", "r", encoding="utf-8") as f:
    data = json.load(f)

record_map = data.get("recordMap", {})
blocks = record_map.get("block", {})

# Buscar un bloque de tipo table
for b_id, b_data in blocks.items():
    val = b_data.get("value", {}).get("value", {})
    if not val:
        val = b_data.get("value", {})
    if not val:
        continue
    
    if val.get("type") == "table":
        print("=== DETALLES DEL BLOQUE TABLE ===")
        print(json.dumps(val, indent=2, ensure_ascii=False))
        
        # Tomar la primera fila
        child_ids = val.get("content", [])
        if child_ids:
            first_row_id = child_ids[0]
            first_row_val = blocks.get(first_row_id, {}).get("value", {}).get("value", {})
            if not first_row_val:
                first_row_val = blocks.get(first_row_id, {}).get("value", {})
            print("\n=== DETALLES DE LA PRIMERA FILA (table_row) ===")
            print(json.dumps(first_row_val, indent=2, ensure_ascii=False))
        break
