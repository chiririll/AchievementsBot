from PIL import Image

Images = ["default.png", "magical.png", "magical_2.png"]

if __name__ == "__main__":
    for Img in Images:
        img = Image.open(f"../Images/styles/{Img}")
        img = img.resize((150, 50))
        img.save(f"../Images/resized/{Img}")
