import argparse
from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw, ImageChops
import os
from typing import List
import random  # For noise seed
import math

def add_pixel_noise(img: Image.Image, intensity: float) -> Image.Image:
    """Jack in some grainy chaos."""
    width, height = img.size
    pixels = img.load()
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            noise = random.randint(-int(intensity * 30), int(intensity * 30))
            pixels[x, y] = (max(0, min(255, r + noise)), max(0, min(255, g + noise)), max(0, min(255, b + noise)))
    return img

def chromatic_aberration(img: Image.Image, intensity: float) -> Image.Image:
    """Cyber fringe: Split RGB channels for neon glow shift."""
    r, g, b = img.split()
    # Shift red + green slightly
    r_shifted = ImageChops.offset(r, int(intensity * 2), 0)
    g_shifted = ImageChops.offset(g, -int(intensity * 1), 0)
    # Merge with offset blue for purple haze
    aberrated = Image.merge("RGB", (r_shifted, g_shifted, b))
    return aberrated

def circuit_etch(img: Image.Image, intensity: float) -> Image.Image:
    """Etch wire-like lines over tattoos for cyber depth."""
    # Sobel edges for circuit crisp (using FIND_EDGES as proxy)
    edges = img.filter(ImageFilter.FIND_EDGES).convert('L')
    # Scale edges for alpha mask (0-255)
    mask = edges.point(lambda p: max(0, min(255, int(p * intensity * 0.5))))
    
    # Create green glow layer as RGBA
    glow_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    # Solid green to paste with mask as alpha
    solid_green = Image.new('L', img.size, 200)  # Mid-high green; adjust for glow
    glow_layer.paste(solid_green, mask=mask)
    
    # Composite onto original
    final = Image.alpha_composite(img.convert('RGBA'), glow_layer).convert('RGB')
    return final

def simulate_oil_paint(img: Image.Image, intensity: float) -> Image.Image:
    """Artsy oil slick: Smear + dither for brushstroke vibe."""
    raw_size = int(3 + intensity * 2)
    size = raw_size if raw_size % 2 == 1 else raw_size + 1
    size = max(3, size)  # Ensure odd and at least 3
    oiled = img.filter(ImageFilter.MedianFilter(size=size))
    dithered = ImageEnhance.Sharpness(oiled).enhance(1 + intensity * 0.5)
    return dithered

def watercolor_wash(img: Image.Image, intensity: float) -> Image.Image:
    """Watercolor bleed: Soften + tint for wet paper flow."""
    washed = img.filter(ImageFilter.GaussianBlur(radius=intensity * 1))
    tint_factor = 1.0 + (intensity * 0.1)  # Warmth build
    tinted = ImageEnhance.Color(washed).enhance(tint_factor)
    return tinted

def emboss_relief(img: Image.Image, intensity: float) -> Image.Image:
    """Emboss for sculpted depth."""
    embossed = img.filter(ImageFilter.EMBOSS)
    relief = ImageEnhance.Contrast(embossed).enhance(intensity * 0.4)
    return Image.blend(img, relief.convert("RGB"), alpha=intensity * 0.4)

def progressive_glitch(img: Image.Image, step: int, max_steps: int) -> Image.Image:
    """Cumulative pixel jacking + cyber/artsy layers: heavier per iteration."""
    intensity = (step / max_steps) * 1.5  # Gentle ramp to 1.5
    
    # Core glitch stack (toned, with sat boost for neon)
    blurred = img.filter(ImageFilter.GaussianBlur(radius=intensity * 1.5))
    contrasted = ImageEnhance.Contrast(blurred).enhance(1 + intensity * 0.5)
    # Surge saturation for splashy cyber pop
    color_surge = ImageEnhance.Color(contrasted).enhance(1.1 + intensity * 0.4)  # Amp from 0.9 to surge
    poster_bits = max(1, 8 - int(intensity * 2))
    posterized = ImageOps.posterize(color_surge, poster_bits)
    noised = add_pixel_noise(posterized, intensity)
    edged = noised.filter(ImageFilter.FIND_EDGES)
    edged = ImageEnhance.Brightness(edged).enhance(intensity * 0.3)
    glitched = Image.blend(noised, edged.convert("RGB"), alpha=intensity * 0.2)
    
    # Cyber layers
    aberrated = chromatic_aberration(glitched, intensity)
    etched = circuit_etch(aberrated, intensity)
    
    # Artsy overlays (build on cyber)
    oiled = simulate_oil_paint(etched, intensity)
    washed = watercolor_wash(oiled, intensity)
    relieved = emboss_relief(washed, intensity)
    
    return relieved

def generate_jack_variants(input_path: str, num_images: int, output_dir: str):
    """Iterate images with escalating pixel jacking + cyber artsy flair."""
    base_image = Image.open(input_path).convert("RGB")
    
    os.makedirs(output_dir, exist_ok=True)
    variants = []
    
    # Save base as jack_0
    base_path = os.path.join(output_dir, "jack_0.png")
    base_image.save(base_path)
    variants.append(base_path)
    print(f"Jack'd: {base_path} (step 0 - pristine cyber sip)")
    
    current = base_image
    for i in range(1, num_images + 1):
        current = progressive_glitch(current, i, max_steps=num_images)
        output_path = os.path.join(output_dir, f"jack_{i}.png")
        current.save(output_path)
        variants.append(output_path)
        print(f"Jack'd: {output_path} (step {i}/{num_images} intensity)")
    
    return variants

def jack_thread_captions(variants: List[str], watermark_text: str = None) -> str:
    """Thread for the cyber artsy pixel decay saga."""
    thread = "🧵 Cyber Splash Pijack: Neon waifu unravels—fringes flare, circuits etch, oils drip in the grid. Bench-born glow. #CyberGlitch #NeonArt\n\n"
    
    effects = [
        "chromatic fringes tease the blue haze",
        "saturation surges, wires glow faint",
        "watercolor bleeds into tattoo veins",
        "oil strokes slick the cyber storm",
        "emboss relief fractures the sip"
    ]
    
    for i, path in enumerate(variants[1:], 1):
        cap = f"{i}/{len(variants)-1}: Ramp {i}—{effects[i-1] if i <= len(effects) else 'matrix meltdown peaks'}. Portrait pulses. "
        if watermark_text:
            cap += f"{watermark_text} "
        cap += f"\n[Neon Fracture: {os.path.basename(path)}]\n\n"
        thread += cap
    
    thread += "Grid collapse. Which pulse hooks you? Quote to hack. 🌐💨"
    
    output_dir = os.path.dirname(variants[0]) if variants else "."
    caption_file = os.path.join(output_dir, "cyber_jack_thread.txt")
    with open(caption_file, "w") as f:
        f.write(thread)
    print(f"Cyber jack thread ready: {caption_file}")
    return thread

def main():
    parser = argparse.ArgumentParser(description="Cyber artsy pixel-jacking iterative variants & thread.")
    parser.add_argument("--input", required=True, help="Your cyber waifu jpg")
    parser.add_argument("--num_images", type=int, default=5, help="Jack steps (excl. original)")
    parser.add_argument("--output_dir", default="./cyber_jack_variants", help="Save spot")
    parser.add_argument("--watermark_text", default=None, help="Tag it")
    
    args = parser.parse_args()
    variants = generate_jack_variants(args.input, args.num_images, args.output_dir)
    thread = jack_thread_captions(variants, args.watermark_text)
    print("\n--- CYBER JACK THREAD ---\n", thread)

if __name__ == "__main__":
    main()