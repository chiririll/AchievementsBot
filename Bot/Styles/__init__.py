import random
from Bot.Achievement import Style


styles = [
    Style("Styles/Default.achst"),
    Style("Styles/Magical.achst")
]


def get(style_id):
    if not style_id:
        return styles[0]
    if style_id < 0:
        return random.choice(styles)
    if style_id < len(styles):
        return styles[style_id]
    return styles[0]
