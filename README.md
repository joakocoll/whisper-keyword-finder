Whisper Audio CLI
Transcribe audios y busca coincidencias por palabras clave o frases usando Whisper + Fuzzy.

Requisitos
Python 3.9+

GPU (opcional pero recomendado)

ffmpeg instalado y en el PATH

pip o conda

Instalación
git clone https://github.com/tuusuario/whisper-cli.git
cd whisper-cli
pip install -r requirements.txt

Uso
python app.py

Seguí las instrucciones del menú para:

Transcribir un archivo de audio.

Buscar audios por palabras clave en un directorio.

Buscar audios por frase usando fuzzy matching.

Cambiar el modelo Whisper.

Notas
Para usar GPU, asegurate de tener instalados CUDA y la versión de PyTorch compatible con GPU.

Si no tenés GPU, el programa correrá en CPU, con menor velocidad.

El programa soporta formatos de audio comunes: .wav, .mp3, .m4a, .ogg.

Licencia
Este proyecto está bajo licencia MIT.

