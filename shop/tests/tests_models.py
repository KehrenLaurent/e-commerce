from django.test import TestCase
from django.db import models

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
            description_courte="Une petite citadine",
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

    def test_reference_label(self):
        produit = Produit.objects.first()
        field_reference = produit._meta.get_field('reference')
        self.assertEqual(field_reference.verbose_name, "Référence du produit")
        self.assertEqual(field_reference.max_length, 150)

    def test_description_courte_label(self):
        produit = Produit.objects.first()
        field_description = produit._meta.get_field('description_courte')
        self.assertEqual(field_description.verbose_name, "Description courte")
        self.assertEqual(field_description.max_length, 250)

    def test_description_longue_label(self):
        produit = Produit.objects.first()
        field_description = produit._meta.get_field('description_longue')
        self.assertEqual(field_description.verbose_name, "Description longue")

    def test_categorie_label(self):
        produit = Produit.objects.first()
        field_categorie = produit._meta.get_field('categorie')
        self.assertEqual(field_categorie.related_model, Categorie)

    def test_sous_categorie_label(self):
        produit = Produit.objects.first()
        field_categorie = produit._meta.get_field('sous_categorie')
        self.assertEqual(field_categorie.related_model, SousCategorie)

    def test_prix_label(self):
        produit = Produit.objects.first()
        field_prix = produit._meta.get_field('prix')
        self.assertEqual(field_prix.verbose_name, "Prix HT du produit")
        self.assertEqual(field_prix.max_digits, 10)
        self.assertEqual(field_prix.decimal_places, 2)

    def test_date_creation_label(self):
        produit = Produit.objects.first()
        field_date_creation = produit._meta.get_field('date_creation')
        self.assertEqual(field_date_creation.verbose_name, "Date de création")
        self.assertTrue(field_date_creation.auto_now_add)

    def test_date_modification_label(self):
        produit = Produit.objects.first()
        field_date_modification = produit._meta.get_field('date_modification')
        self.assertEqual(field_date_modification.verbose_name,
                         "Date de modification")
        self.assertTrue(field_date_modification.auto_now)

    def test_actif_label(self):
        produit = Produit.objects.first()
        field_date_modification = produit._meta.get_field('actif')
        self.assertEqual(field_date_modification.verbose_name, "Produit actif")
        self.assertFalse(field_date_modification.default)

    def test_miniature_label(self):
        produit = Produit.objects.first()
        field_miniature = produit._meta.get_field('miniature')
        self.assertEqual(field_miniature.upload_to, "shop/media")
        self.assertEqual(field_miniature.verbose_name, "Miniature du produit")
        self.assertTrue(field_miniature.null)
