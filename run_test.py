import os
import sys
from PIL import Image
from torchvision import transforms

# Definir transformación para redimensionar la imagen
resize_transform = transforms.Resize((1000, 1000))

def preprocess_image(image_path, output_folder, max_size_kb):
    # Abrir la imagen y redimensionarla
    img = Image.open(image_path).convert('RGB')
    img_resized = resize_transform(img)
    
    # Guardar la imagen redimensionada en el disco
    output_filename = os.path.basename(image_path)
    output_filepath = os.path.join(output_folder, output_filename)
    img_resized.save(output_filepath, format='JPEG', quality=80)  # Guardar como JPEG con calidad baja
    
    return output_filepath

def run_test(image_folder):
    # Crear la carpeta 'compressed' si no existe
    compressed_folder = os.path.join(image_folder, 'compressed')
    os.makedirs(compressed_folder, exist_ok=True)
    
    # Obtener la lista de archivos en la carpeta original
    files = os.listdir(image_folder)

    # Iterar sobre cada archivo en la carpeta
    for file in files:
        # Verificar si el archivo es una imagen (por ejemplo, extensión .jpg)
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            # Obtener la ruta completa del archivo de imagen original
            image_path = os.path.join(image_folder, file)

            # Preprocesar la imagen redimensionándola y guardándola comprimida
            preprocessed_image_path = preprocess_image(image_path, compressed_folder, max_size_kb=300)
            print(f"Imagen {file} preprocesada y guardada en: {preprocessed_image_path}")

            # Ejecutar los comandos para cada imagen preprocesada
            commands = [
                f"python3 main_lost.py --image_path \"{preprocessed_image_path}\" --visualize pred",
                f"python3 main_lost.py --image_path \"{preprocessed_image_path}\" --visualize fms",
                f"python3 main_lost.py --image_path \"{preprocessed_image_path}\" --visualize seed_expansion"
            ]
            
            # Iterar sobre los comandos y ejecutarlos
            for command in commands:
                print(f"Ejecutando comando: {command}")
                os.system(command)

if __name__ == "__main__":
    # Verificar si se proporcionó una ruta como argumento
    if len(sys.argv) != 2:
        print("Uso: python script.py <ruta_a_carpeta_imagenes>")
        sys.exit(1)
    
    # Obtener la ruta de la carpeta de imágenes del primer argumento
    image_folder = sys.argv[1]
    
    # Verificar si la ruta es válida
    if not os.path.isdir(image_folder):
        print(f"Error: La ruta {image_folder} no es un directorio válido.")
        sys.exit(1)
    
    # Llamar al método run_test para procesar las imágenes desde la carpeta
    run_test(image_folder)
