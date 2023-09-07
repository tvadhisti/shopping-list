from django.shortcuts import render

def show_main(request):
    context = {
        'name': 'Tiva Adhisti Nafira putri',
        'class': 'PBP KI'
    }

    return render(request, 'main.html', context)
