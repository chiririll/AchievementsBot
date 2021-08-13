from PIL import Image
from Achievement import AchievementStyle


styles = [
    AchievementStyle(
        (900, 300), (300, 300), 'Styles/0/font.otf',
        message="Новое достижение!", msg_size=45, msg_pos=((310, 10), (890, 100)),
        name_size=70, name_pos=((310, 10), (890, 250))
    ),
    AchievementStyle(
        (900, 300), (300, 300), 'Styles/1/font.otf',
        message="Открыто достижение!", msg_size=50, msg_pos=((310, 10), (890, 100)),
        bg_image=Image.open('Styles/1/bg.png'), fg_image=Image.open('Styles/1/fg.png'),
        name_size=70, name_pos=((310, 100), (890, 220)),
        use_copyright=False
    ),
    AchievementStyle(
        (900, 300), (300, 300), 'Styles/2/font.ttf',
        message="Открыто достижение!", msg_size=50, msg_pos=((310, 10), (890, 100)), msg_color=(144, 66, 178),
        bg_image=Image.open('Styles/1/bg.png'), fg_image=Image.open('Styles/1/fg.png'),
        name_size=70, name_pos=((310, 100), (890, 220))
    )
]

# TODO: add mask
if __name__ == "__main__":
    for style in styles:
        ach = style.generate("test", Image.open("Images/unknown.jpg"))
        open(f'Images/styles/test_{styles.index(style)}.png', 'wb').write(ach.getbuffer())
