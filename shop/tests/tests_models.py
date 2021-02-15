from django.test import TestCase

from ..models import Categorie, Produit, SousCategorie

# Create your tests here.


class ProductTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):

        cat1 = Categorie.objects.create(
            nom='Voiture',
            description='Voiture pour le grand public'
        )

        ssCat1 = SousCategorie.objects.create(
            nom="Citadine",
            description="Petite voiture consu pour la ville",
            categorie=cat1
        )

        ssCat2 = SousCategorie.objects.create(
            nom="Monospace",
            description="Voiture permettant le transport de beaucoup de personne",
            categorie=cat1
        )

        prod = Produit.objects.create(
            nom='205',
            reference='Peugeot',
            description_court="Une petite citadine",
            description_longue="Une super petite citadine avec 4 places",
            categorie=cat1,
            prix=15000,
            actif=True,
        )

        prod.sous_categorie.add(ssCat1)

    def test_nom_label(self):
        produit = Produit.objects.first()
        field_nom = produit._meta.get_field('nom')
        self.assertEqual(field_nom.verbose_name, "Nom du produit")
        self.assertEqual(field_nom.max_length, 150)
