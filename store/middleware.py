class UTMTrackingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        utm_source = request.GET.get('utm_source')
        utm_medium = request.GET.get('utm_medium')
        utm_campaign = request.GET.get('utm_campaign')

        if utm_source:
            request.session['utm_source'] = utm_source

        if utm_medium:
            request.session['utm_medium'] = utm_medium

        if utm_campaign:
            request.session['utm_campaign'] = utm_campaign

        response = self.get_response(request)
        return response