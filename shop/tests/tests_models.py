from django.test import TestCase
from ..models import Category, Product

# Create your tests here.


class CategoryTestCase(TestCase):
    def setUp(self):
        self.film = Category.objects.create(name='Film', slug='film')
        self.chanson_francais = Category.objects.create(
            name='Chanson français', slug='chanson-français')

    def test_category_init(self):
        self.assertEqual(self.chanson_francais.name, 'Chanson français')
        self.assertEqual(self.chanson_francais.slug, 'chanson-français')

    def test_str(self):
        self.assertEqual(self.chanson_francais.name,
                         str(self.chanson_francais))


class ProductTestCase(TestCase):
    def setUp(self):
        self.film = Category.objects.create(name='Film', slug='film')
        self.chanson_francais = Category.objects.create(
            name='Chanson français', slug='chanson-français')

        self.les_visiteurs = Product.objects.create(
            category=self.film,
            name='Les visiteurs',
            slug='les-visiteurs',
            description='Un film qui parle de chevaliers qui voyage dans le temps',
            price=15.99,
            available=True
        )

    def test_product_init(self):
        self.assertEqual(self.les_visiteurs.category, self.film)
        self.assertEqual(self.les_visiteurs.name, 'Les visiteurs')
        self.assertEqual(self.les_visiteurs.slug, 'les-visiteurs')
        self.assertEqual(self.les_visiteurs.description,
                         'Un film qui parle de chevaliers qui voyage dans le temps')
        self.assertEqual(self.les_visiteurs.price, 15.99)
        self.assertEqual(self.les_visiteurs.available, True)
