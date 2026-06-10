import json
import sys
import os

# Forzar codificación UTF-8 para consola de Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open("notion_response.json", "r", encoding="utf-8") as f:
    data = json.load(f)

record_map = data.get("recordMap", {})
blocks = record_map.get("block", {})

output_lines = []

def get_block_text(block_val):
    properties = block_val.get("properties", {})
    title_prop = properties.get("title", [])
    text = ""
    for item in title_prop:
        if isinstance(item, list) and len(item) > 0:
            text += item[0]
    return text

def parse_table_block(block_val):
    col_order = block_val.get("format", {}).get("table_block_column_order", [])
    row_ids = block_val.get("content", [])
    
    if not col_order or not row_ids:
        return ""
        
    table_lines = []
    
    for i, row_id in enumerate(row_ids):
        row_wrapper = blocks.get(row_id, {})
        row_val = row_wrapper.get("value", {}).get("value", {})
        if not row_val:
            row_val = row_wrapper.get("value", {})
            
        if not row_val or row_val.get("type") != "table_row":
            continue
            
        row_properties = row_val.get("properties", {})
        
        # Extraer celdas en orden de columnas
        row_cells = []
        for col_id in col_order:
            cell_prop = row_properties.get(col_id, [])
            cell_text = ""
            for item in cell_prop:
                if isinstance(item, list) and len(item) > 0:
                    cell_text += item[0]
            
            # Limpiar saltos de línea para que no rompa la tabla Markdown
            cell_text = cell_text.replace("\n", " ").strip()
            row_cells.append(cell_text)
            
        # Formatear la fila de la tabla
        row_line = "| " + " | ".join(row_cells) + " |"
        table_lines.append(row_line)
        
        # Insertar separador en la segunda línea
        if i == 0:
            separator = "| " + " | ".join(["---"] * len(col_order)) + " |"
            table_lines.append(separator)
            
    return "\n".join(table_lines) + "\n"

def parse_block_recursive(block_id, depth=0):
    block_wrapper = blocks.get(block_id, {})
    value = block_wrapper.get("value", {}).get("value", {})
    if not value:
        value = block_wrapper.get("value", {})
    if not value:
        return
        
    block_type = value.get("type", "text")
    text = get_block_text(value)
    
    # Ignorar table_row aquí porque se procesan dentro de su respectivo table
    if block_type == "table_row":
        return
        
    # Sangría o formato según nivel de profundidad si es lista
    indent = "  " * depth if block_type in ["bulleted_list", "numbered_list"] else ""
    
    if block_type == "page" and depth > 0:
        output_lines.append(f"\n{'#' * min(depth+1, 6)} Página Enlazada: {text}")
    elif block_type == "header":
        output_lines.append(f"\n# {text}")
    elif block_type == "sub_header":
        output_lines.append(f"\n## {text}")
    elif block_type == "sub_sub_header":
        output_lines.append(f"\n### {text}")
    elif block_type == "bulleted_list":
        output_lines.append(f"{indent}* {text}")
    elif block_type == "numbered_list":
        output_lines.append(f"{indent}1. {text}")
    elif block_type == "to_do":
        checked = "[x]" if value.get("properties", {}).get("checked", [["No"]])[0][0] == "Yes" else "[ ]"
        output_lines.append(f"{indent}{checked} {text}")
    elif block_type == "callout":
        output_lines.append(f"\n> ℹ️ {text}")
    elif block_type == "image":
        caption = text if text else "imagen"
        output_lines.append(f"\n![{caption}](attachment_placeholder)")
    elif block_type == "toggle":
        output_lines.append(f"\n▶️ {text}")
    elif block_type == "quote":
        output_lines.append(f"\n> {text}")
    elif block_type == "table":
        table_md = parse_table_block(value)
        output_lines.append(f"\n{table_md}")
    else:
        if text.strip():
            output_lines.append(f"{indent}{text}")

    # Procesar hijos de manera recursiva (excepto tablas que ya manejan sus filas internamente)
    if block_type != "table":
        child_ids = value.get("content", [])
        for child_id in child_ids:
            parse_block_recursive(child_id, depth + 1)

# Iniciar recorrido desde la página principal
page_id = "2ef91803-9206-80fa-8f57-c56dd7178e4b"
parse_block_recursive(page_id, 0)

# Guardar en archivo markdown
output_path = os.path.join(os.path.dirname(__file__), "notion_doc.md")
with open(output_path, "w", encoding="utf-8") as out_f:
    out_f.write("\n".join(output_lines))

print(f"Documento completo con tablas extraído en: {output_path}")

# También imprimir una vista previa a consola
print("\n=== VISTA PREVIA DEL DOCUMENTO COMPLETO ===")
for line in output_lines[:45]:
    print(line)
if len(output_lines) > 45:
    print(f"\n... (truncado, ver el archivo completo en {output_path})")
