from .forms import ContactForm, NouveauContactForm
from django.shortcuts import render

from .models import Contact


def contact(request):
    # Construire le formulaire, soit avec les données postées,
    # soit vide si l'utilisateur accède pour la première fois
    # à la page.
    form = ContactForm(request.POST or None)
    # Nous vérifions que les données envoyées sont valides
    # Cette méthode renvoie False s'il n'y a pas de données
    # dans le formulaire ou qu'il contient des erreurs.
    if form.is_valid():
        # Ici nous pouvons traiter les données du formulaire
        sujet = form.cleaned_data['sujet']
        message = form.cleaned_data['message']
        envoyeur = form.cleaned_data['envoyeur']
        renvoi = form.cleaned_data['renvoi']

        # Nous pourrions ici envoyer l'e-mail grâce aux données
        # que nous venons de récupérer
        envoi = True

    # Quoiqu'il arrive, on affiche la page du formulaire.
    return render(request, 'scraper_admin/contact.html', locals())


def nouveau_contact(request):
    sauvegarde = False
    form = NouveauContactForm(request.POST or None, request.FILES)
    if form.is_valid():
        contact = Contact()
        contact.nom = form.cleaned_data["nom"]
        contact.adresse = form.cleaned_data["adresse"]
        contact.photo = form.cleaned_data["photo"]
        contact.save()
        sauvegarde = True

    return render(request, 'scraper_admin/contact.html', {
        'form': form,
        'sauvegarde': sauvegarde
    })


def voir_contacts(request):
    return render(
        request,
        'scraper_admin/image.html',
        {'contacts': Contact.objects.all()}
    )


def launch_spider(request):
    return render(
        request,
        'scraper_admin/launch_spider.html',
        {'contacts': Contact.objects.all()}
    )


def chart(request):
    return render(
        request,
        'scraper_admin/chart.html',
        {'contacts': Contact.objects.all()}
    )
