import unittest
from Achievement import *


class AchievementTests(unittest.TestCase):

    def test_Default(self):
        st = Style(open('Styles/Default.achst', 'rb'))
        ach = Achievement(st, "testing", "Images/unknown.jpg")
        ach.generate().save('Images/styles/default.png', 'PNG')

    def test_Magical(self):
        st = Style(open('Styles/Magical.achst', 'rb'))
        ach = Achievement(st, "testing", "Images/unknown.jpg")
        ach.generate().save('Images/styles/magical.png', 'PNG')

    def test_Magical_2(self):
        st = Style(open('Styles/Magical 2.achst', 'rb'))
        ach = Achievement(st, "testing", "Images/unknown.jpg")
        ach.generate().save('Images/styles/magical 2.png', 'PNG')

    def test_Layout(self):
        st = Style(open('Styles/Layout.achst', 'rb'))
        ach = Achievement(st, "testing", "Images/unknown.jpg")
        ach.generate().save('Images/styles/layout.png', 'PNG')


if __name__ == '__main__':
    unittest.main()
