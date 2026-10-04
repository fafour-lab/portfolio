from io import BytesIO
from pathlib import Path
from PIL import Image, ImageCms, ImageOps


OUTPUT_DIR = Path(__file__).resolve().parents[1] / "dist" / "assets" / "images"

SOURCES = {
    "portrait.jpg": "/private/tmp/aboukacem-photo-review/portrait-heif.jpg",
    "music-01.jpg": "/Users/macbookpro/Documents/ChatGPT/My Website/Photos/Music/_R5A9193.JPG",
    "music-02.jpg": "/Users/macbookpro/Documents/ChatGPT/My Website/Photos/Music/_R5A9461-Enhanced-NR 2.JPG",
    "music-03.jpg": "/Users/macbookpro/Documents/ChatGPT/My Website/Photos/Music/_R5A9449-Enhanced-NR 2.JPG",
    "music-04.jpg": "/Users/macbookpro/Documents/ChatGPT/My Website/Photos/Music/IMG_4737.JPG",
    "music-05.jpg": "/Users/macbookpro/Documents/ChatGPT/My Website/Photos/Music/IMG_4751.JPG",
    "music-06.jpg": "/Users/macbookpro/Documents/ChatGPT/My Website/Photos/Music/2DF44202-D06A-4DA1-B756-A0EF76D0F823.jpeg",
    "music-07.jpg": "/Users/macbookpro/Documents/ChatGPT/My Website/Photos/Music/Pergola-Show-19.jpg",
    "research-01.jpg": "/Users/macbookpro/Documents/ChatGPT/My Website/Photos/Research/IMG_9062.JPG",
    "research-02.jpg": "/Users/macbookpro/Documents/ChatGPT/My Website/Photos/Research/IMG_0250.JPG",
    "research-03.jpg": "/private/tmp/aboukacem-photo-review/research-03-heif.jpg",
    "research-04.jpg": "/private/tmp/aboukacem-photo-review/research-04-heif.jpg",
    "research-05.jpg": "/private/tmp/aboukacem-photo-review/research-05-heif.jpg",
    "research-06.jpg": "/Users/macbookpro/Documents/ChatGPT/My Website/Photos/Research/bd135c73-3087-4e68-bf2e-5d9c435c1d18.jpg",
    "research-07.jpg": "/private/tmp/aboukacem-photo-review/IMG_9380.HEIC.png",
}


def to_srgb(image: Image.Image) -> Image.Image:
    icc = image.info.get("icc_profile")
    if icc:
        try:
            source_profile = ImageCms.ImageCmsProfile(BytesIO(icc))
            target_profile = ImageCms.createProfile("sRGB")
            return ImageCms.profileToProfile(image, source_profile, target_profile, outputMode="RGB")
        except (ImageCms.PyCMSError, OSError, TypeError, ValueError):
            pass
    return image.convert("RGB")


def process(source: str, destination: Path) -> None:
    with Image.open(source) as original:
        image = ImageOps.exif_transpose(original)
        image = to_srgb(image)
        image.thumbnail((1800, 1800), Image.Resampling.LANCZOS)
        image.save(
            destination,
            format="JPEG",
            quality=84,
            optimize=True,
            progressive=True,
            subsampling=1,
        )
        print(f"{destination.name}: {image.width}x{image.height} ({destination.stat().st_size} bytes)")


OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
for filename, source in SOURCES.items():
    process(source, OUTPUT_DIR / filename)
