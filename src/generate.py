# src/generate.py
import argparse, os, json, random
from PIL import Image, ImageDraw, ImageFont

def gpu_available():
    try:
        import torch
        return torch.cuda.is_available()
    except Exception:
        return False

def sd_generate(prompt, w, h, steps, guidance, model_id):
    import torch
    from diffusers import StableDiffusionPipeline
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device=="cuda" else torch.float32
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=dtype).to(device)
    pipe.safety_checker = None
    img = pipe(prompt, num_inference_steps=steps, guidance_scale=guidance, width=w, height=h).images[0]
    return img

def placeholder(prompt, w, h):
    img = Image.new("RGB",(w,h),(250,250,250))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", max(22,w//36))
    except:
        font = ImageFont.load_default()
    d.rectangle([20,20,w-20,h-20], outline=(40,40,40), width=4)
    d.text((40,40), "Platzhalter-Bild\n\n"+prompt, fill=(0,0,0), font=font)
    return img

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", required=True, help="Kurzbeschreibung/Bildprompt")
    ap.add_argument("--output_dir", default="out/pages")
    ap.add_argument("--policy", default="configs/policy.json")
    args = ap.parse_args()

    pol = json.load(open(args.policy,"r",encoding="utf-8"))
    w, h = pol.get("width",704), pol.get("height",960)
    steps, guidance, model_id = pol.get("num_inference_steps",24), pol.get("guidance_scale",7.0), pol.get("model","runwayml/stable-diffusion-v1-5")

    os.makedirs(args.output_dir, exist_ok=True)
    out = os.path.join(args.output_dir, "page_01.png")

    if gpu_available():
        try:
            img = sd_generate(args.text, w, h, steps, guidance, model_id)
        except Exception as e:
            print("[warn] SD-Generierung fehlgeschlagen, Platzhalter:", e)
            img = placeholder(args.text, w, h)
    else:
        img = placeholder(args.text, w, h)

    img.save(out)
    print("[ok]", out)

if __name__ == "__main__":
    main()
