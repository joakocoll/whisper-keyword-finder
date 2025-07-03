import os
import whisper
from fuzzywuzzy import fuzz

# Funciones
def transcribirAudio(modelo, audio_path):
    result = modelo.transcribe(audio_path)
    return result['text']

def compararPalabrasClaves(transcripcion, palabras_clave):
    words = transcripcion.lower().split()
    return sum(words.count(p.lower()) for p in palabras_clave)

def encontrarAudioPorPalabras(modelo, directorio, palabras_clave):
    mejor_archivo = None
    max_coincidencias = 0
    for archivo in os.listdir(directorio):
        if archivo.lower().endswith(('.mp3', '.wav', '.m4a', '.ogg')):
            path = os.path.join(directorio, archivo)
            texto = transcribirAudio(modelo, path)
            coincidencias = compararPalabrasClaves(texto, palabras_clave)
            if coincidencias > max_coincidencias:
                max_coincidencias = coincidencias
                mejor_archivo = archivo
    return mejor_archivo, max_coincidencias

def is_phrase_similar(transcripcion, phrase, threshold=70):
    ratio = fuzz.partial_ratio(phrase.lower(), transcripcion.lower())
    return ratio >= threshold, ratio

def encontrarAudioPorFrase(modelo, directorio, frase, threshold=70):
    mejor_archivo = None
    mejor_ratio = 0
    for archivo in os.listdir(directorio):
        if archivo.lower().endswith(('.mp3', '.wav', '.m4a', '.ogg')):
            path = os.path.join(directorio, archivo)
            texto = transcribirAudio(modelo, path)
            similar, ratio = is_phrase_similar(texto, frase, threshold)
            if similar and ratio > mejor_ratio:
                mejor_ratio = ratio
                mejor_archivo = archivo
    return mejor_archivo, mejor_ratio

# Selección de modelo
modelos_disponibles = ["tiny", "base", "small", "medium", "large"]
modelo = None

def elegir_modelo():
    global modelo
    print("\nModelos disponibles:")
    for i, nombre in enumerate(modelos_disponibles, 1):
        print(f"{i}. {nombre}")
    while True:
        entrada = input("Elegí un número de modelo: ").strip()
        if entrada.isdigit() and 1 <= int(entrada) <= len(modelos_disponibles):
            seleccionado = modelos_disponibles[int(entrada) - 1]
            print(f"\n🔄 Cargando modelo '{seleccionado}'...")
            modelo = whisper.load_model(seleccionado)
            print("✅ Modelo cargado.")
            break
        else:
            print("❌ Número inválido. Intentá de nuevo.")

# Inicializar modelo
elegir_modelo()

# Menú principal
while True:
    print("\nElige una opción:")
    print("1. Obtener texto de un audio")
    print("2. Encontrar audio por palabras clave")
    print("3. Encontrar audio por frase (fuzzy)")
    print("4. Cambiar modelo")
    print("5. Salir")

    opcion = input("Opción: ").strip()

    if opcion == "1":
        ruta = input("Ruta al archivo de audio: ").strip()
        if os.path.isfile(ruta):
            texto = transcribirAudio(modelo, ruta)
            print("\n📝 Transcripción:\n", texto)
        else:
            print("❌ Archivo no encontrado.")

    elif opcion == "2":
        directorio = input("Directorio con los audios: ").strip()
        if not os.path.isdir(directorio):
            print("❌ Directorio inválido.")
            continue
        palabras = input("Palabras clave separadas por coma: ").strip().split(",")
        palabras = [p.strip() for p in palabras]
        archivo, count = encontrarAudioPorPalabras(modelo, directorio, palabras)
        if archivo:
            print(f"✅ Mejor coincidencia: {archivo} ({count} coincidencias)")
        else:
            print("❌ No se encontraron coincidencias.")

    elif opcion == "3":
        directorio = input("Directorio con los audios: ").strip()
        if not os.path.isdir(directorio):
            print("❌ Directorio inválido.")
            continue
        frase = input("Frase a buscar (fuzzy): ").strip()
        archivo, ratio = encontrarAudioPorFrase(modelo, directorio, frase)
        if archivo:
            print(f"✅ Mejor coincidencia: {archivo} (similaridad: {ratio})")
        else:
            print("❌ No se encontraron coincidencias suficientes.")

    elif opcion == "4":
        elegir_modelo()

    elif opcion == "5":
        print("👋 Saliendo...")
        break

    else:
        print("⚠️ Opción inválida. Elegí entre 1 y 5.")
