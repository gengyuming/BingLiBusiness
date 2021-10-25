from .settings import *


AES_KEY = '1Q2w3e4r%'

DATABASES = {
    'default': {
        'NAME': 'quality',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'TEST': {
            'NAME': 'django_template_testdb',
            'CHARSET': 'utf8'
        },
        'CHARSET': 'utf8'
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': '127.0.0.1:11211',  # 本地地址
        'TIMEOUT': 3600,  # 单位：秒
        'OPTIONS': {
            'MAX_ENTRIES': 1000,  # 高速缓存允许的最大条目数，超出这个数则旧值将被删除. 这个参数默认是300.
            'CULL_FREQUENCY': 3,  # 当达到MAX_ENTRIES 的时候,被删除的条目比率。 实际比率是 1 / CULL_FREQUENCY，默认是3
        }
    }
}
