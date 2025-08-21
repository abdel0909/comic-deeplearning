# src/export_pdf.py
import argparse, os, glob
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Image as RLImage, PageBreak, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--images", default="out/pages", help="Ordner mit Seitenbildern (links)")
    ap.add_argument("--textfile", default="configs/sample_textpage.txt", help="Textdatei (rechte Seite)")
    ap.add_argument("--output", default="out/comic.pdf", help="Ziel-PDF")
    args = ap.parse_args()

    os.makedirs("out", exist_ok=True)
    imgs = sorted(glob.glob(os.path.join(args.images, "*.png")))
    if not imgs:
        raise SystemExit("Keine Bilder gefunden. Erst generate.py ausführen.")

    text = open(args.textfile, "r", encoding="utf-8").read()

    doc = SimpleDocTemplate(args.output, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Für jede Bildseite eine Textseite dahinter
    for i, img in enumerate(imgs, start=1):
        story.append(RLImage(img, width=400, height=560))
        story.append(PageBreak())
        story.append(Paragraph("<b>Textseite</b>", styles["Title"]))
        story.append(Spacer(1, 8))
        story.append(Paragraph(text.replace("\n","<br/>"), styles["Normal"]))
        story.append(PageBreak())

    doc.build(story)
    print("[ok]", args.output)

if __name__ == "__main__":
    main()
