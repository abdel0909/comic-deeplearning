git clone https://github.com/DEINNAME/comic-deeplearning.git
cd comic-deeplearning
pip install -r requirements.txt

# 1) Bildseite erzeugen (GPU → SD-Bild, ohne GPU → Platzhalter)
python -m src.generate --text "bear and eagle meet on museum steps, symbolic comic, clean lineart" --output_dir out/pages

# 2) Textseite definieren (Bearbeite configs/sample_textpage.txt) und PDF bauen
python -m src.export_pdf --images out/pages --textfile configs/sample_textpage.txt --output out/comic.pdf

# 3) Bilder bewerten (z. B. CLIP-Score)
python -m src.score --images out/pages --prompt "bear and eagle meet on museum steps" --out runs/scores.json

# 4) (Stub) Verbesserung / Feintuning-Start
python -m src.improve
