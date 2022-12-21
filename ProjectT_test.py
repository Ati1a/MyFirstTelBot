import unittest
import ProjectT


class TestProjectT(unittest.TestCase):
    def test_last_news(self):  # тесты действительны до появления новых новостей на портале ВШЭ
        self.assertEqual(ProjectT.last_news('https://ba.hse.ru/news/admission/'), 'Опубликована стоимость обучения для поступающих в 2023 году')
        self.assertNotEqual(ProjectT.last_news('https://ba.hse.ru/news/admission/'), 'Опубликованы траектории и схемы поступления в 2023 году')

    def test_search_name(self):
        self.assertEqual(ProjectT.search_name('177-037-237 75'), '177-037-237 75 найден на 43 странице в файле Приказ 6.18.1-05_160822-59')
        self.assertNotEqual(ProjectT.search_name('177-037-237 75'), 'Я не смог найти вас в приказах о зачисление')
        self.assertEqual(ProjectT.search_name('000-000-000 00'), 'Я не смог найти вас в приказах о зачисление')


if __name__ == "__main__":
    unittest.main()
