from django.shortcuts import render


def bbglist(request):

    context = {
        'bbg': "BBG List of Projects will display here"

    }
    return render(request, 'bbg/bbglist.html', context)
