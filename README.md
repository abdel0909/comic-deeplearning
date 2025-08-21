# Comic Deep Learning

Erzeugt Comic-Doppelseiten (linke Seite Bild, rechte Seite Text) und kann sich über Iterationen verbessern (Scoring + LoRA-Feintuning – Platzhalter im Code).

## Quickstart (Colab)
```python
!git clone https://github.com/DEINNAME/comic-deeplearning.git
%cd comic-deeplearning
!pip -q install -r requirements.txt
!python -m src.generate --text "Der 🐻 Bär trifft den 🦅 Adler vor dem Museum." --output_dir out
!python -m src.export_pdf --images out/pages --textfile configs/sample_textpage.txt --output out/comic.pdf
