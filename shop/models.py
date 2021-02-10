from django.db import models

# Class abstraite


class CategorieBase(models.Model):
    nom = models.CharField(max_length=100)
    description = models.CharField(max_length=250)

    class Meta:
        abstract = True

    def __str__(self):
        return self.nom


class Categorie(CategorieBase):

    class Meta:
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'


class SousCategorie(CategorieBase):
    categories = models.ForeignKey(
        Categorie, related_name="sous_categorie", on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Sous catégorie'
        verbose_name_plural = 'Sous catégories'


# Class du projet
class Produit(models.Model):
    nom = models.CharField(max_length=150, verbose_name="Nom du produit")
    reference = models.CharField(
        max_length=150, verbose_name="Référence du produit")
    description_court = models.CharField(
        max_length=250, verbose_name="Description courte")
    description_longue = models.TextField(verbose_name='Description longue')
    categorie = models.ForeignKey(
        Categorie, related_name="produits", on_delete=models.SET_NULL)
    sous_categorie = models.ManyToManyField(
        SousCategorie, related_name="produits", on_delete=models.CASCADE)
    prix = models.DecimalField(
        verbose_name="Prix HT du produit", max_digits=10, decimal_places=2)
    date_creation = models.DateTimeField(
        verbose_name="Date de création", auto_now_add=True)
    date_modification = models.DateTimeField(
        verbose_name="Date de modification", auto_now=True)
    actif = models.BooleanField(verbose_name="Produit actif", default=False)

    class Meta:
        verbose_name = 'Produit'
        verbose_name_plural = 'Produits'
        ordering = ('nom',)

    def __str__(self):
        return self.nom
