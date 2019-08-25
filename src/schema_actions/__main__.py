import logging

from get_schema import SchemaFetcher
from post_schema import SchemaPoster
from delete_schema import SchemaDeleter
from db_init import SchemDBInit

logging.basicConfig(level=logging.INFO)


def init(args):
    return SchemDBInit().init(args)


def get(args):
    return SchemaFetcher().fetch(args)


def post(args):
    return SchemaPoster().post(args)


def delete(args):
    return SchemaDeleter().delete(args)
