
from django.http import HttpResponse

def say_hello(request):
    print ("Hello from views.say_hello")
    return HttpResponse("Hello, Django!")

def say_goodbye(request):
    print ("Hello from views.say_goodbye")
    return HttpResponse("Goodbye, Django!")


def search(request):
    query = request.GET['query'] 
    page = request.GET["page"]

    # Perform search or filter based on query parameters
    # Return appropriate response
    response = f"Search query: {query}, Page: {page}"
    return HttpResponse(response)

