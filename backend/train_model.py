import os
import sys

# Configurar stdout para usar UTF-8 y soportar emojis/caracteres en consolas de Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Asegurar que el directorio de la app esté en el path de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.ml_service import ml_service
from app.config import settings

def main():
    print("====================================================")
    print("  INICIANDO ENTRENAMIENTO DEL MODELO CLÍNICO REAL")
    print("====================================================")
    
    dataset_path = settings.DATASET_PATH
    print(f"Ruta configurada del dataset: {dataset_path}")
    
    if not os.path.exists(dataset_path):
        print(f"⚠️ ERROR: No se encontró el dataset en '{dataset_path}'")
        print("Asegúrate de que el nombre del archivo sea exactamente 'Hipertension_Arterial_Mexico (1).csv'")
        print(f"Archivos en backend/data/: {os.listdir('data') if os.path.exists('data') else 'Carpeta no encontrada'}")
        return
        
    try:
        print("\nCargando datos, aplicando Label Engineering, SMOTE y entrenando XGBoost...")
        metrics = ml_service.train_model(dataset_path)
        
        print("\n====================================================")
        print("   ¡ENTRENAMIENTO COMPLETADO EXITOSAMENTE!")
        print("====================================================")
        print(f"Precisión global (Accuracy): {metrics['accuracy']*100:.2f}%")
        print("\nSENSIBILIDAD (RECALL) POR CLASE DE RIESGO:")
        print(f"  🟢 Bajo:  {metrics['recall_bajo']*100:.2f}%")
        print(f"  🟡 Medio: {metrics['recall_medio']*100:.2f}%")
        print(f"  🔴 Alto:  {metrics['recall_alto']*100:.2f}%")
        
        print("\nPRECISIÓN POR CLASE:")
        print(f"  🟢 Bajo:  {metrics['precision_bajo']*100:.2f}%")
        print(f"  🟡 Medio: {metrics['precision_medio']*100:.2f}%")
        print(f"  🔴 Alto:  {metrics['precision_alto']*100:.2f}%")
        
        print(f"\nTotal registros ENSANUT analizados: {metrics['total_registros_ensanut']}")
        print(f"Distribución original de etiquetas: {metrics['distribucion_clases_original']}")
        print(f"Modelo guardado exitosamente en: {settings.MODEL_PATH}")
        print("====================================================")
        
    except Exception as e:
        print(f"❌ Ocurrió un error durante el entrenamiento: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
