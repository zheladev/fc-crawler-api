from pyramid.config import Configurator


def includeme(config: Configurator):
    config.include(".core")
    config.include(".renderer")
