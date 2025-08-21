# src/score.py
import argparse, glob, json, os

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--images", default="out/pages")
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--out", default="runs/scores.json")
    args = ap.parse_args()

    os.makedirs("runs", exist_ok=True)
    try:
        from transformers import CLIPProcessor, CLIPModel
        import torch
        device="cuda" if torch.cuda.is_available() else "cpu"
        model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
        proc  = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        scores=[]
        for p in sorted(glob.glob(f"{args.images}/*.png")):
            from PIL import Image
            im=Image.open(p).convert("RGB")
            inp=proc(text=[args.prompt], images=im, return_tensors="pt", padding=True).to(device)
            s=model(**inp).logits_per_image.squeeze().item()
            scores.append({"path":p,"clip":float(s)})
        json.dump(scores, open(args.out,"w"))
        print("[ok] scores ->", args.out)
    except Exception as e:
        print("[warn] CLIP nicht verfügbar:", e)

if __name__=="__main__":
    main()
