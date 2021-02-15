from django.db import models
from django.contrib.auth.models import User

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
class Image(models.Model):
    produit = models.ForeignKey(
        'Produit', verbose_name='images', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='shop/media')


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
    miniature = models.FileField(
        upload_to="shop/media", null=True, verbose_name="Miniature du produit")

    class Meta:
        verbose_name = 'Produit'
        verbose_name_plural = 'Produits'
        ordering = ('nom',)

    def __str__(self):
        return self.nom


class Client(models.Model):
    """
    Un client est une personne inscrite sur le site dans le but de faire une commande
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    adresse_envoi_defaut = models.ForeignKey("Adresse",
                                             related_name="adresse_envoi_defaut",
                                             null=True,
                                             verbose_name="Adresse de livraison par défaut",
                                             on_delete=models.SET_NULL)
    adresse_facturation_defaut = models.ForeignKey("Adresse",
                                                   related_name="adresse_facturation_defaut",
                                                   null=True,
                                                   verbose_name="Adresse de facturation par défaut",
                                                   on_delete=models.SET_NULL)

    def __str__(self):
        return self.user


class Adresse(models.ForeignKey):
    """
    Une adresse est liée au client pour la facturation ou la livraison
    """
    MONSIEUR = "M"
    MADAME = "Mme"
    GENRE = (
        (MONSIEUR, "Monsieur"),
        (MADAME, "Madame")
    )

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    genre = models.CharField(max_length=3, choices=GENRE,
                             default=MONSIEUR, verbose_name="Civilité")
    nom = models.CharField(max_length=50, verbose_name="Nom")
    prenom = models.CharField(max_length=50, verbose_name="Prénom")
    societe = models.CharField(max_length=50, verbose_name="Société")
    adresse = models.CharField(max_length=250, verbose_name="Adresse")
    complement_adresse = models.CharField(
        max_length=250, verbose_name="Complément d'adresse", blank=True)
    pays = models.CharField(max_length=50, verbose_name="Pays")
    code_poste = models.CharField(max_length=5, verbose_name="Code Postal")
    ville = models.CharField(max_length=50, verbose_name="Ville")
    telephone = models.CharField(
        max_length=10, verbose_name="Téléphone", blank=True)
    mobile = models.CharField(max_length=10, verbose_name="mobile", blank=True)
    fax = models.CharField(max_length=10, verbose_name="fax", blank=True)

    class Meta:
        verbose_name = 'Adresse'
        verbose_name_plural = 'Adresses'

    def __str__(self):
        return "{} {} ({}, {} {})".format(self.nom, self.prenom, self.adresse, self.code_poste, self.ville)


class Commande(models.Model):
    ATTENTE = "ATT"
    PAYEE = "PAY"
    EXPEDIEE = "EXP"
    ANNULEE = "ANN"
    STATUT = (
        (ATTENTE, "En attente"),
        (PAYEE, "Payée"),
        (EXPEDIEE, "expédiée"),
        (ANNULEE, "annulée")
    )
    client = models.ForeignKey(
        Client, verbose_name='commandes', on_delete=models.CASCADE)
    adresse = models.ForeignKey(
        Adresse, related_name='commandes', on_delete=models.CASCADE)
    date_commande = models.DateTimeField(
        verbose_name="Date de commande", auto_now_add=True)
    date_envoi = models.DateTimeField(verbose_name="Date de l'envoi", )
    statut = models.CharField(max_length=3, choices=STATUT, default=ATTENTE)


class Fournisseur(models.Model):
    pass


class DetailCommande(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    quantite = models.IntegerField(verbose_name="Quantité", default=1)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL)

    def __str__(self):
        return "Commande {}, produit {}".format(self.commande, self.produit)
