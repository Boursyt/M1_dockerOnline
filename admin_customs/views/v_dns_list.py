from django.shortcuts import render, redirect
from dns.service.s_ovh import lsdns
from django.http import JsonResponse

def admin_dns_liste_page(request):
    """
    Handles the admin DNS list page. This function renders a page displaying the
    DNS registrations if the user is authenticated. If the user is not authenticated,
    it redirects them to the home page.

    :param request: The HTTP request object that contains metadata about the request.

    :return: An HTTP response object containing the rendered template for the admin
        DNS list page if the user is authenticated, otherwise a redirection response
        to the home page.
    """
    user = request.user

    if user.is_authenticated:
        registrements = admin_listeDNS()
        context = {
            'menu': {
                'page': 'list'
            },
            'registrements': registrements
        }
        return render(request, 'admin_list_dns.html', context)
    else:
        return redirect('/home')


def admin_listeDNS():
    """
    Retrieves and formats a list of DNS records into a structured list of dictionaries.
    The function processes DNS records by extracting specific information, including
    the identifier and name of each DNS entry, and returns a list of dictionaries
    containing these attributes.

    :return: A list of dictionaries where each dictionary contains the "id" and "name"
             attributes of a DNS entry.
    :rtype: list[dict]
    """

    dns_list = lsdns()
    registrement = []

    for dns in dns_list:
        registrement.append({
            "id": dns["id"],
            "name": dns["name"],

        })

    return registrement