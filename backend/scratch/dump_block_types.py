import json

with open("notion_response.json", "r", encoding="utf-8") as f:
    data = json.load(f)

record_map = data.get("recordMap", {})
blocks = record_map.get("block", {})

print(f"Total bloques en recordMap: {len(blocks)}")

types = {}
for b_id, b_data in blocks.items():
    val = b_data.get("value", {}).get("value", {})
    if not val:
        val = b_data.get("value", {})
    if not val:
        continue
    b_type = val.get("type", "unknown")
    types[b_type] = types.get(b_type, 0) + 1

print("\nConteo de tipos de bloques:")
for b_type, count in types.items():
    print(f"  {b_type}: {count}")

print("\n--- EJEMPLOS DE TEXTO POR TIPO ---")
for target_type in types.keys():
    print(f"\n[{target_type}] ejemplos:")
    example_count = 0
    for b_id, b_data in blocks.items():
        val = b_data.get("value", {}).get("value", {})
        if not val:
            val = b_data.get("value", {})
        if not val or val.get("type") != target_type:
            continue
            
        title_prop = val.get("properties", {}).get("title", [])
        text = ""
        for item in title_prop:
            if isinstance(item, list) and len(item) > 0:
                text += item[0]
                
        # Para tablas o colecciones, a veces las propiedades son distintas
        if target_type == "table_row":
            cells = val.get("properties", {})
            text = " | ".join(["".join([c[0] for c in cells[col] if c]) for col in sorted(cells.keys())])
            
        if text.strip() or target_type in ["table", "table_row"]:
            print(f"  - ID: {b_id} | Text: {text[:150]}")
            example_count += 1
            if example_count >= 3:
                break
