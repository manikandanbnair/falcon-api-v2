from configparser import ConfigParser

from elasticsearch import Elasticsearch


class ElasticConnection:
    def __init__(self,config_file = 'config.ini'):
        config = ConfigParser()
        config.read(config_file)

        self.host = config.get('elasticsearch','host',fallback='localhost')
        self.port = int(config.get('elasticsearch','port',fallback=9200))
        self.username = config.get('elasticsearch','username',fallback=None)
        self.password = config.get('elasticsearch', 'password', fallback=None)


    def connect_to_elastic(self):
        hosts = [{'host': self.host, 'port': self.port,'scheme':"http"}]
        es_client = Elasticsearch(
            hosts,
            http_auth=(self.username,self.password)
        )

        return es_client