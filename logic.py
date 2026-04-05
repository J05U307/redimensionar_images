import os
from PIL import Image
from datetime import datetime

def process_images(images, output, w, h, keep, fmt, new_name=None):
    try:
        if not images:
            return "⚠️ No hay imágenes"

        w, h = int(w), int(h)

        # Si no hay carpeta destino → crear en Descargas
        if not output:
            downloads = os.path.join(os.path.expanduser("~"), "Descargas")
            folder_name = f"procesadas_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            output = os.path.join(downloads, folder_name)
            os.makedirs(output, exist_ok=True)

        exts = (".png", ".jpg", ".jpeg", ".webp")

        count = 0

        for i, path in enumerate(images):
            if not path.lower().endswith(exts):
                continue

            try:
                with Image.open(path) as img:

                    if keep:
                        img.thumbnail((w, h))
                    else:
                        img = img.resize((w, h))

                   # Nombre nuevo o original
                    if new_name and new_name.strip():
                        name = f"{new_name}_{i+1}"
                    else:
                        name = os.path.splitext(os.path.basename(path))[0]

                    out = os.path.join(output, f"{name}.{fmt.lower()}")

                    if fmt == "JPG" and img.mode == "RGBA":
                        img = img.convert("RGB")

                    if fmt == "ICO":
                        img.save(out, format="ICO", sizes=[(w, h)])
                    else:
                        img.save(out, fmt)

                    count += 1

            except Exception as e:
                print(f"Error con {path}: {e}")

        return f"✅ {count} imágenes procesadas en:\n{output}"

    except Exception as e:
        return f"❌ Error general: {e}"