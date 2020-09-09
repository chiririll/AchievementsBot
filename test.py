from PIL import Image
from Achievement import AchievementStyle


a = AchievementStyle(
            (900, 300), (300, 300), 'Styles/2/font.ttf',
            message="Открыто достижение!", msg_size=50, msg_pos=((310, 10), (890, 100)), msg_color=(144, 66, 178),
            bg_image=Image.open('Styles/1/bg.png'), fg_image=Image.open('Styles/1/fg.png'),
            name_size=70, name_pos=((310, 100), (890, 220))
        )
a.generate("test", Image.open("Images/unknown.jpg")).save('test.png')
