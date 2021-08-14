from PIL import ImageDraw, Image, ImageFilter

if __name__ == "__main__":
    mask = Image.new("L", (300, 300), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse(((5, 5), (300 - 5, 300 - 5)), fill=255)
    # Blur
    mask = mask.filter(ImageFilter.GaussianBlur(3))
    mask.save('mask.png', "PNG")
