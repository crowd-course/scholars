from calendar import timegm
from urlparse import parse_qsl

import datetime
import requests
from django.conf import settings
from django.urls import reverse
from rest_framework import parsers, renderers, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from social_core.exceptions import MissingBackend
from social_core.utils import get_strategy, setting_name
from social_django.utils import psa, load_strategy, load_backend
from social_django.views import NAMESPACE

from scholars.users.serializers import UserSerializer


# class ObtainAuthToken(APIView):
#     throttle_classes = ()
#     permission_classes = ()
#     parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
#     renderer_classes = (renderers.JSONRenderer,)
#     serializer_class = AuthTokenSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#
#         from django.contrib.auth import login
#         if user is not None:
#             login(request, user)
#
#         user_serializer = UserSerializer(instance=user)
#         return Response({'token': token.key, 'user': user_serializer.data})


# obtain_auth_token = ObtainAuthToken.as_view()


def auth_by_token(request, backend, token):
    strategy = load_strategy(request=request)

    try:
        backend = load_backend(strategy, backend, reverse(NAMESPACE + ":complete", args=(backend,)))
    except MissingBackend:
        msg = 'Invalid backend'
        raise AuthenticationFailed(msg)

    try:
        user = backend.do_auth(access_token=token)
    except requests.HTTPError as e:
        msg = e.response.text
        raise AuthenticationFailed(msg)

    if not user:
        msg = 'Bad credentials'
        raise AuthenticationFailed(msg)

    return user


def get_access_token_from_provider(request, backend):
    access_token = None

    if backend == 'google-oauth2':
        access_token_url = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_ACCESS_TOKEN_URL
        secret = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET

        # Add more backends here if needed

        params = {
            'client_id': request.data.get('clientId'),
            'redirect_uri': request.data.get('redirectUri'),
            'client_secret': secret,
            'code': request.data.get('code'),
            'grant_type': 'authorization_code'
        }

        # Step 1. Exchange authorization code for access token.
        r = requests.post(access_token_url, params=params)

        try:
            access_token = r.json().get('access_token')
        except KeyError:
            access_token = None

    return access_token


class SocialView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        backend = request.data.get(u'backend', 'google-oauth2')

        auth_token = get_access_token_from_provider(request, backend)

        if auth_token is not None and backend:
            try:
                # Try to authenticate the user using python-social-auth
                user = auth_by_token(request, backend, auth_token)

                if user:
                    if not user.is_active:
                        return Response({'status': 'Unauthorized',
                                         'message': 'The user account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)

                    # Get the JWT payload for the user.
                    payload = jwt_payload_handler(user)

                    # todo work on refresh tokens later
                    # Include original issued at time for a brand new token,
                    # to allow token refresh
                    # if settings.REST_FRAMEWORK_JWT_ALLOW_REFRESH:
                    #     payload['orig_iat'] = timegm(
                    #         datetime.datetime.utcnow().utctimetuple()
                    #     )

                    # Create the response object with the JWT payload.
                    user_serializer = UserSerializer(instance=user)

                    response_data = {
                        'token': jwt_encode_handler(payload),
                        'user': user_serializer.data
                    }

                    return Response(response_data)
            except Exception as e:
                print e
                return Response({'status': 'Bad request',
                                 'message': 'Could not authenticate with the provided token.'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': 'Bad request',
                             'message': 'Authentication could not be performed with received data.'},
                            status=status.HTTP_400_BAD_REQUEST)
