from django.shortcuts import get_object_or_404

from frontend.models import Helper


def username(request):
    helper = logged_in_helper = None
    if 'helper' in request.resolver_match.kwargs:
        helper_pk = request.resolver_match.kwargs['helper']
        helper = get_object_or_404(Helper, pk=helper_pk)
    if 'helper' in request.session:
        helper_pk = request.session['helper']
        logged_in_helper = get_object_or_404(Helper, pk=helper_pk)

    return {'HELPER': helper, 'LOGGED_IN_HELPER': logged_in_helper}
