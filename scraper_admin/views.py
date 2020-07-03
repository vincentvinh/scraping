from urllib.parse import urlparse
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .forms import ContactForm, NouveauContactForm
from django.shortcuts import render
from scrapyd_api import ScrapydAPI
from pprint import pprint

from .models import ScrapyOrder, ScrapyItem

# connect scrapyd service
scrapyd = ScrapydAPI('http://localhost:6800')


class SchedulingError(Exception):
    def __str__(self):
        return 'scheduling error'


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


@csrf_exempt
@require_http_methods(['GET', 'POST'])  # only get and post
def launch_spider(request):
    pprint(request.method)
    scrapy_items = ScrapyItem.objects.all()
    if request.method == 'POST':
        pprint('1')
        url = request.POST.get('url', None)  # take url comes from client. (From an input may be?)
        pprint(url)
        if not url:
            return JsonResponse({'error': 'Missing  args'})

        if not is_valid_url(url):
            return JsonResponse({'error': 'URL is invalid'})

        domain = urlparse(url).netloc  # parse the url and extract the domain
        unique_id = str(uuid4())  # create a unique ID.

        settings = {
            'unique_id': unique_id,  # unique ID for each record for DB
            'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        }

        scrapyd.schedule('default', 'crawler',
                                settings=settings, url=url, domain=domain)

    elif request.method == 'GET':
        # We were passed these from past request above. Remember ?
        # They were trying to survive in client side.
        # Now they are here again, thankfully. <3
        # We passed them back to here to check the status of crawling
        # And if crawling is completed, we respond back with a crawled data.
        pprint('2')
        task_id = request.GET.get('task_id', None)
        unique_id = request.GET.get('unique_id', None)
        status = 'empty'

        if not task_id or not unique_id:

            return render(
                request,
                'scraper_admin/launch_spider.html',
                {'scrapys': scrapy_items}
            )

        # Here we check status of crawling that just started a few seconds ago.
        # If it is finished, we can query from database and get results
        # If it is not finished we can return active status
        # Possible results are -> pending, running, finished
        status = scrapyd.job_status('default', task_id)
        if status == 'finished':
            try:
                # this is the unique_id that we created even before crawling started.
                item = ScrapyItem.objects.get(unique_id=unique_id)

                return render(
                    request,
                    'scraper_admin/launch_spider.html',
                    {'scrapys': scrapy_items, 'status': status}
                )
            except Exception as e:
                return JsonResponse({'error': str(e)})
        else:
            status = 'pending'
            return render(
                request,
                'scraper_admin/launch_spider.html',
                {'scrapys': scrapy_items, 'status': status}
            )
    else:
        return render(
            request,
            'scraper_admin/launch_spider.html',
            {'scrapys': scrapy_items}
        )
    status = 'get success'
    return render(
        request,
        'scraper_admin/launch_spider.html',
        {'scrapys': scrapy_items, 'status': status}
    )



def chart(request):
    return render(
        request,
        'scraper_admin/chart.html',
        {'Scrapys': ScrapyItem.objects.all()}
    )


def is_valid_url(url):
    validate = URLValidator()
    try:
        validate(url)  # check if url format is valid
    except ValidationError:
        return False

    return True
