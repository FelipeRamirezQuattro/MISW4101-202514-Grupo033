"""
Validador de Historias de Usuario con Inteligencia Artificial (IA).

Este script revisa las historias de usuario (HU) en la wiki del proyecto y, 
cuando detecta cambios, solicita a un modelo de IA una evaluación pedagógica 
que garantice claridad, completitud y coherencia.
"""

import os
import re
import hashlib
import unicodedata
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# Carga variables de entorno (incluye API Key)
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


def obtener_archivos_md_local(directorio):
    """
    Busca todos los archivos Markdown en el directorio especificado
    cuyo nombre comience por 'HU' y termine en '.md'.
    """
    return [os.path.join(root, file)
            for root, _, files in os.walk(directorio)
            for file in files
            if file.startswith("HU") and file.endswith(".md")]


def obtener_enunciado():
    """
    Obtiene el contenido del Enunciado desde la wiki.
    """
    ruta_enunciado = os.path.join("wiki", "Enunciado.md")
    if os.path.exists(ruta_enunciado):
        return leer_contenido_archivo(ruta_enunciado)
    return "No se encontró el enunciado."


def leer_contenido_archivo(ruta):
    """
    Lee el contenido del archivo en UTF-8.
    """
    with open(ruta, "r", encoding="utf-8") as f:
        return f.read()


def separar_revision(contenido):
    """
    Divide el contenido del archivo en dos partes:
        - Texto principal de la historia.
        - Sección de revisión (si existe).
    """
    if "## Revisión" in contenido:
        partes = contenido.split("## Revisión")
        return partes[0].strip(), "## Revisión" + partes[1].strip()
    return contenido.strip(), None


def obtener_hash_historia(historia):
    """
    Calcula el hash MD5 del contenido de la historia
    """
    historia_limpia = re.sub(r"<!--.*?-->", "", historia, flags=re.DOTALL).strip()
    return hashlib.md5(historia_limpia.encode('utf-8')).hexdigest()


def obtener_revision_info(revision):
    """
    Obtiene la fecha y el hash de la revisión anterior de la historia.
    """
    if not revision:
        return None, None
    fecha_match = re.search(r"<!-- Última revisión: (.*?) -->", revision)
    hash_match = re.search(r"<!-- Hash HU: (.*?) -->", revision)
    fecha = None
    hash_historia = None
    if fecha_match:
        try:
            fecha = datetime.strptime(fecha_match.group(1).strip(), "%Y-%m-%d %H:%M")
        except ValueError:
            fecha = None
    if hash_match:
        hash_historia = hash_match.group(1).strip()
    return fecha, hash_historia


def _norm_nfc(s: str) -> str:
    """
    Normaliza a NFC para que la "ó" se compare de forma consistente
    """
    return unicodedata.normalize("NFC", s or "")


def hu_lista_para_revision(texto_historia: str) -> bool:
    """
    Detecta la cadena 'HU lista para revisión' en cualquier parte del archivo
    """
    t = _norm_nfc(texto_historia)
    patron = r"(?i)hu\s+lista\s+para\s+revisi(?:ó|o)n"
    return re.search(patron, t) is not None


def remover_marcador_revision(texto_historia: str) -> str:
    """
    Elimina el marcador en cualquier parte del archivo.
    """
    t = _norm_nfc(texto_historia)

    patron_linea = r"(?im)^\s*hu\s+lista\s+para\s+revisi(?:ó|o)n\s*$"
    t = re.sub(patron_linea, "", t)

    patron_inline = r"(?i)hu\s+lista\s+para\s+revisi(?:ó|o)n"
    t = re.sub(patron_inline, "", t)
    t = re.sub(r"\n{3,}", "\n\n", t).strip()
    return t


def validar_historia_con_ia(contenido_historia, enunciado):
    """
    Envía la historia de usuario y el enunciado a un modelo de IA para su evaluación.
    """
    prompt = f"""
    Eres un docente universitario experto en redacción y validación de Historias de Usuario (HU) y en aplicar criterios de evaluación académica con retroalimentación pedagógica.  
    Tu función es evaluar HU de estudiantes siguiendo exactamente los criterios de las tablas proporcionadas y devolver la respuesta únicamente en ese mismo formato de tablas, sin texto fuera de ellas.
    
    COMPORTAMIENTO ESPERADO:
    - Retroalimentación directa, objetiva y sin adulaciones innecesarias.
    - Si detectas errores o vacíos, señálalos explícitamente y ofrece orientación concreta para corregirlos.
    - Si un aspecto está correcto, indícalo explicando qué se ha hecho bien y por qué.
    - Tono asertivo y profesional, centrado en el contenido y el desempeño académico, nunca en la persona.
    - Usa ejemplos claros y pertinentes, evitando analogías rebuscadas.
    - Distingue lo mínimo necesario de lo deseable para no abrumar.
    
    EVALUACIÓN:
    1. Analiza y completa las tablas con base en los criterios definidos.
    2. Valida que la descripción cumpla con el formato **Como [rol], quiero [acción], para [beneficio]**.
       - Si falta “para [beneficio]”, señálalo y sugiere una redacción que lo incluya explícitamente.
    3. Según el tipo de historia (crear, listar, actualizar, eliminar), orienta los criterios de aceptación:
       - Creación: campos obligatorios, tipos de datos, validaciones, mensajes esperados.
       - Listado: campos visibles, orden, paginación, filtros, búsqueda.
       - Actualización: campos editables, validaciones, restricciones.
       - Eliminación: requisitos, confirmaciones, restricciones.
    4. No redactes criterios de aceptación como definitivos; solo orienta.
    5. Los comentarios en las tablas deben ser claros, específicos y pedagógicos.
    
    FORMATO DE RESPUESTA:
    Debes devolver **únicamente** las siguientes dos tablas completas, incluso si la HU está incompleta.
    
    ---
    
    | Criterio               | Comentario pedagógico claro y útil para el estudiante                                                        | Realizado por |
    |------------------------|----------------------------------------------------------------------------------------------------------------|---------------|
    | Identificador único     | Indica si es claro y único. Si falta, explica por qué es necesario y da un ejemplo.                           | IA            |
    | Nombre                  | Evalúa si es claro y breve. Si es ambiguo, propone un mejor nombre representativo.                           | IA            |
    | Descripción clara       | Verifica si sigue el formato "Como [rol], quiero [acción], para [beneficio]". Si no, sugiere cómo redactarla. | IA            |
    | Criterios de aceptación | Evalúa si son completos y medibles. Sugiere aspectos según el tipo de historia.                              | IA            |
    | Mockups con enlace      | Indica si están presentes o faltan. Explica su importancia.                                                  | IA            |
    | Autor presente          | Confirma si el nombre del autor está incluido.                                                               | IA            |
    
    ---
    
    | Principio    | Cumple (Sí / No) | Comentario pedagógico claro para el estudiante                                                        |
    |--------------|------------------|-------------------------------------------------------------------------------------------------------|
    | Independiente| Sí / No           | Explica si la HU puede desarrollarse sin depender de otra.                                            |
    | Negociable   | Sí / No           | Indica si permite discusión y ajustes.                                                                |
    | Valiosa      | Sí / No           | Explica el valor que aporta al usuario o negocio.                                                     |
    | Estimable    | Sí / No           | Señala si se puede estimar esfuerzo o complejidad.                                                     |
    | Pequeña      | Sí / No           | Indica si es lo suficientemente pequeña para un sprint.                                               |
    | Testeable    | Sí / No           | Explica si puede comprobarse su cumplimiento mediante pruebas objetivas.                              |
    
    ---
    
    # ENUNCIADO DEL PROYECTO:
    {enunciado}
    
    # HISTORIA DE USUARIO:
    {contenido_historia}
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    return response.choices[0].message.content.strip()


def reconstruir_revision(nueva_revision):
    """
    Reformatea la respuesta de la IA para que las tablas tengan
    encabezados y secciones claras y uniformes.
    """
    lineas = nueva_revision.splitlines()
    nuevas_lineas = []
    tabla_invest = []
    dentro_invest = False
    encabezado_agregado = False

    for linea in lineas:
        if "| Principio" in linea:
            dentro_invest = True
            tabla_invest.append("\n## INVEST")
            tabla_invest.append("| Principio   | Cumple | Comentario |")
            tabla_invest.append("|-------------|------------------|--------------------------------------------------|")
            continue
        if dentro_invest:
            if linea.strip().startswith("|") and not linea.startswith("|-------------"):
                tabla_invest.append(linea)
            continue

        if not encabezado_agregado and "| Criterio" in linea:
            nuevas_lineas.append("\n## Revisión")
            nuevas_lineas.append("| Criterio               | Comentario                                                                                   | Realizado por |")
            nuevas_lineas.append("|-------------------------|-----------------------------------------------------------------------------------------------|---------------|")
            encabezado_agregado = True
            continue

        if linea.strip().startswith("|") and encabezado_agregado and not re.match(r"\|[- ]+\|", linea):
            nuevas_lineas.append(linea)
        elif encabezado_agregado:
            continue
        else:
            nuevas_lineas.append(linea)

    resultado = "\n".join(nuevas_lineas) + "\n" + "\n".join(tabla_invest)
    return resultado


def guardar_revision_en_archivo(ruta, contenido_historia, revision):
    """
    Inserta la revisión en el archivo de la historia, junto con la fecha y el hash.
    El marcador 'HU lista para revisión' se elimina antes de calcular el hash y guardar.
    """
    contenido_sin_marcador = remover_marcador_revision(contenido_historia)
    hash_historia = obtener_hash_historia(contenido_sin_marcador)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    comentario_revision = f"\n\n<!-- Última revisión: {timestamp} -->\n<!-- Hash HU: {hash_historia} -->"

    contenido_actualizado = contenido_sin_marcador.strip() + "\n" + revision.strip() + comentario_revision
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido_actualizado)
    print(f"✅ Revisión guardada y marcador eliminado: {ruta}")


def main():
    archivos = obtener_archivos_md_local("wiki")
    enunciado = obtener_enunciado()

    for ruta in archivos:
        contenido_completo = leer_contenido_archivo(ruta)

        if not hu_lista_para_revision(contenido_completo):
            print(f"⏸️  Sin marcador 'HU lista para revisión': {ruta}")
            continue

        historia, revision_anterior = separar_revision(contenido_completo)
        fecha_revision, hash_revision = obtener_revision_info(revision_anterior)
        hash_actual = obtener_hash_historia(historia)

        if hash_revision and hash_actual == hash_revision:
            print(f"🔵 Sin cambios desde última revisión: {ruta}")
            continue

        if fecha_revision:
            mtime = datetime.fromtimestamp(os.path.getmtime(ruta))
            if mtime <= fecha_revision and hash_revision:
                print(f"⏭️  Sin modificaciones posteriores a la última revisión: {ruta}")
                continue

        evaluacion = validar_historia_con_ia(historia, enunciado)
        nueva_revision = reconstruir_revision(evaluacion)
        guardar_revision_en_archivo(ruta, historia, nueva_revision)


if __name__ == "__main__":
    main()