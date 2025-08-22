import io
import os
import zipfile
from datetime import datetime
from typing import List

from flask import Flask, request, send_file, render_template_string, redirect, url_for, flash
from werkzeug.utils import secure_filename

# Pure-Python / manylinux wheels (no OS deps):
# pypdf for PDF merging/splitting, Pillow for image handling, PyMuPDF for PDF->images
from pypdf import PdfWriter, PdfReader
from PIL import Image
import fitz  # PyMuPDF

# ---- Config ----
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")
# Limit upload size (adjust for your host). 50 MB total is friendly to free tiers.
app.config["MAX_CONTENT_LENGTH"] = int(os.environ.get("MAX_UPLOAD_MB", "50")) * 1024 * 1024
ALLOWED_PDF = {"pdf"}
ALLOWED_IMG = {"png", "jpg", "jpeg", "webp", "bmp", "tiff"}

# ---- UI Template (kept inline so it's truly one file) ----
PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>PDF Toolkit • Merge & Convert</title>
  <style>
    body { font-family: -apple-system, system-ui, Segoe UI, Roboto, sans-serif; max-width: 880px; margin: 24px auto; padding: 0 12px; }
    h1 { font-size: 1.6rem; margin-bottom: 0.5rem; }
    section { border: 1px solid #ddd; border-radius: 10px; padding: 16px; margin: 18px 0; }
    input[type=file] { width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 8px; }
    button { padding: 10px 14px; border: 0; border-radius: 8px; background: #111; color: #fff; font-weight: 600; }
    .tip { color: #555; font-size: .9rem; }
    .msg { background: #ffe9a8; padding: 10px; border-radius: 8px; margin-bottom: 8px; }
    footer { color:#666; font-size:.85rem; margin-top:32px; }
    .grid { display: grid; gap: 12px; }
  </style>
</head>
<body>
  <h1>PDF Toolkit — Merge & Convert</h1>
  {% with messages = get_flashed_messages() %}
    {% if messages %}
      {% for m in messages %}<div class="msg">{{ m }}</div>{% endfor %}
    {% endif %}
  {% endwith %}

  <section>
    <h2>1) Merge PDFs → single PDF</h2>
    <form class="grid" action="{{ url_for('merge') }}" method="post" enctype="multipart/form-data">
      <input type="file" name="files" accept="application/pdf" multiple required />
      <button type="submit">Merge PDFs</button>
      <div class="tip">Tip: Use the Files picker on iOS to select multiple PDFs. Order is kept as selected; if your host reorders, we sort by filename.</div>
    </form>
  </section>

  <section>
    <h2>2) Images → PDF</h2>
    <form class="grid" action="{{ url_for('images_to_pdf') }}" method="post" enctype="multipart/form-data">
      <input type="file" name="images" accept="image/*" multiple required />
      <label>Page size:
        <select name="pagesize">
          <option value="auto" selected>Auto (fit to image)</option>
          <option value="A4">A4 Portrait</option>
          <option value="Letter">Letter Portrait</option>
        </select>
      </label>
      <button type="submit">Convert to PDF</button>
      <div class="tip">Supported: PNG, JPG, JPEG, WEBP, BMP, TIFF.</div>
    </form>
  </section>

  <section>
    <h2>3) PDF → Images (PNG)</h2>
    <form class="grid" action="{{ url_for('pdf_to_images') }}" method="post" enctype="multipart/form-data">
      <input type="file" name="pdf" accept="application/pdf" required />
      <label>DPI: <input type="number" name="dpi" value="144" min="72" max="300" /></label>
      <button type="submit">Convert to PNG (ZIP)</button>
      <div class="tip">Returns a .zip of PNGs, one per page. Higher DPI = larger files.</div>
    </form>
  </section>

  <footer>
    <div>Max upload total: {{ max_mb }} MB. Time: {{ now }}</div>
  </footer>
</body>
</html>
"""

def _ext_ok(filename: str, allowed: set) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed

@app.route("/", methods=["GET"])
def index():
    return render_template_string(PAGE, max_mb=int(app.config["MAX_CONTENT_LENGTH"]/1024/1024), now=datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"))

@app.post("/merge")
def merge():
    files = request.files.getlist("files")
    if not files:
        flash("No files uploaded.")
        return redirect(url_for("index"))

    pdfs = []
    for f in files:
        filename = secure_filename(f.filename or "")
        if not filename or not _ext_ok(filename, ALLOWED_PDF):
            flash(f"Skipping non-PDF: {filename}")
            continue
        pdfs.append( (filename, io.BytesIO(f.read())) )

    if not pdfs:
        flash("No valid PDFs found.")
        return redirect(url_for("index"))

    # Sort by filename to keep a deterministic order if host reorders uploads
    pdfs.sort(key=lambda x: x[0].lower())

    writer = PdfWriter()
    for name, buf in pdfs:
        buf.seek(0)
        reader = PdfReader(buf)
        for page in reader.pages:
            writer.add_page(page)

    out = io.BytesIO()
    writer.write(out)
    writer.close()
    out.seek(0)
    out_name = f"merged_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.pdf"
    return send_file(out, as_attachment=True, download_name=out_name, mimetype="application/pdf")

@app.post("/images-to-pdf")
def images_to_pdf():
    files = request.files.getlist("images")
    pagesize = (request.form.get("pagesize") or "auto").lower()
    if not files:
        flash("No images uploaded.")
        return redirect(url_for("index"))

    images: List[Image.Image] = []
    for f in files:
        name = secure_filename(f.filename or "")
        if not name or not _ext_ok(name, ALLOWED_IMG):
            flash(f"Skipping non-image: {name}")
            continue
        img = Image.open(io.BytesIO(f.read()))
        # Convert all to RGB for PDF
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        images.append(img)

    if not images:
        flash("No valid images found.")
        return redirect(url_for("index"))

    # Optional page size
    def to_a4(img: Image.Image):
        # A4 at 72 DPI ~ 595x842 pt. We'll fit the image within while preserving aspect.
        A4 = (595, 842)
        return _fit_to_canvas(img, A4)

    def to_letter(img: Image.Image):
        # Letter at 72 DPI ~ 612x792 pt.
        LTR = (612, 792)
        return _fit_to_canvas(img, LTR)

    processed = []
    for img in images:
        if pagesize == "a4":
            processed.append(to_a4(img))
        elif pagesize == "letter":
            processed.append(to_letter(img))
        else:
            processed.append(img)

    out = io.BytesIO()
    if len(processed) == 1:
        processed[0].save(out, format="PDF")
    else:
        processed[0].save(out, format="PDF", save_all=True, append_images=processed[1:])
    out.seek(0)
    out_name = f"images_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.pdf"
    return send_file(out, as_attachment=True, download_name=out_name, mimetype="application/pdf")

def _fit_to_canvas(img: Image.Image, canvas_size):
    # Letter/A4: paste image centered onto a white canvas while preserving aspect
    bg = Image.new("RGB", canvas_size, (255, 255, 255))
    img_ratio = img.width / img.height
    can_ratio = canvas_size[0] / canvas_size[1]
    if img_ratio > can_ratio:
        # Fit to width
        new_w = canvas_size[0]
        new_h = int(new_w / img_ratio)
    else:
        new_h = canvas_size[1]
        new_w = int(new_h * img_ratio)
    resized = img.resize((new_w, new_h))
    x = (canvas_size[0] - new_w) // 2
    y = (canvas_size[1] - new_h) // 2
    bg.paste(resized, (x, y))
    return bg

@app.post("/pdf-to-images")
def pdf_to_images():
    f = request.files.get("pdf")
    if not f:
        flash("No PDF uploaded.")
        return redirect(url_for("index"))
    name = secure_filename(f.filename or "")
    if not _ext_ok(name, ALLOWED_PDF):
        flash("Please upload a .pdf file.")
        return redirect(url_for("index"))

    dpi = int(request.form.get("dpi") or 144)
    data = io.BytesIO(f.read())
    data.seek(0)

    doc = fitz.open(stream=data.getvalue(), filetype="pdf")
    # Render pages to PNG, collect in a ZIP
    zbuf = io.BytesIO()
    with zipfile.ZipFile(zbuf, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for i, page in enumerate(doc, start=1):
            # scale matrix from DPI; 72 base DPI
            zoom = dpi / 72.0
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat, alpha=False)
            img_bytes = pix.tobytes("png")
            z.writestr(f"page_{i:03d}.png", img_bytes)
    doc.close()

    zbuf.seek(0)
    out_name = f"pdf_images_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.zip"
    return send_file(zbuf, as_attachment=True, download_name=out_name, mimetype="application/zip")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)