import unittest
from Achievement import *


class AchievementTests(unittest.TestCase):

    def test_Default(self):
        st = Style(open('Styles/Default.achst', 'rb'))
        ach = Achievement(st, "testing")
        ach.generate().save('Images/styles/default.png', 'PNG')

    def test_Magical(self):
        st = Style(open('Styles/Magical.achst', 'rb'))
        ach = Achievement(st, "testing")
        ach.generate().save('Images/styles/magical.png', 'PNG')

    def test_Magical_2(self):
        st = Style(open('Styles/Magical_2.achst', 'rb'))
        st.change_lang('RUS')
        ach = Achievement(st, "testing")
        ach.generate().save('Images/styles/magical_2.png', 'PNG')

    def test_Layout(self):
        st = Style(open('Styles/Layout.achst', 'rb'))
        ach = Achievement(st, "testing")
        ach.generate().save('Images/styles/layout.png', 'PNG')


if __name__ == '__main__':
    unittest.main()
