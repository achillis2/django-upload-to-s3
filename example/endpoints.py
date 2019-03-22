# coding: utf-8

import uuid

from django.conf import settings
from django.http import JsonResponse
from django.views.generic import View

from boto.s3.connection import S3Connection


def get_form_args_to_s3(key):
    try:
        is_secure = settings.AWS_S3_SECURE_URLS
    except AttributeError:
        is_secure = False
    s3 = S3Connection(settings.AWS_ACCESS_KEY_ID,
                      settings.AWS_SECRET_ACCESS_KEY,
                      is_secure=is_secure)
    http_method = 'https' if is_secure else 'http'
    ret = s3.build_post_form_args(bucket_name=settings.AWS_STORAGE_BUCKET_NAME, key=key,expires_in=3600,acl='public-read', max_content_length=10000000,http_method=http_method).encode("utf-8")
    return ret


class S3AuthAPIView(View):

    def get_s3_key_and_file_path(self, file_name):
        file_name = file_name
        file_path = 'documents/{}/{}'.format(uuid.uuid4(), file_name)
        return '/'.join(['media', file_path]), file_path

    def get(self, request, *args, **kwargs):
        key, file_path = self.get_s3_key_and_file_path(request.GET['file_name'])
        form_args = get_form_args_to_s3(key)
        fields = {'form_args': {}}
        fields['form_args']['action'] = form_args['action']
        fields['form_args']['fields'] = {
            x['name']: x['value'] for x in form_args['fields']}
        fields['file_path'] = file_path
        return JsonResponse(fields)
