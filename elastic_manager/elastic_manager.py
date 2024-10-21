from elastic_manager.connection import ElasticConnection

class ElasticManager:
    es_client= ElasticConnection().connect_to_elastic()


    @classmethod
    def insert(cls, user_data, index_name):
        try:
            cls.es_client.index(
                index=index_name,
                document=user_data
            )
        except Exception:
            raise Exception("Error creating user")

    @classmethod
    def find_all(cls, index_name):
        try:
            response = cls.es_client.search(
                index=index_name,
                body={
                    "query": {
                        "match_all": {}
                    }
                }
            )
            users = []
            for hit in response['hits']['hits']:
                users.append(hit['_source'])
            return users
        except Exception as e:
            raise Exception(f"Error fetching users: {str(e)}")

    @classmethod
    def find_by_email(cls, email, index_name):
        try:

            response = cls.es_client.search(
                index=index_name,
                body={
                    "query": {
                        "match": {
                            "email": {
                                "query": email                            }
                        }
                    }
                }
            )
            if response['hits']['total']['value'] > 0:
                return response['hits']['hits'][0]['_source']
            else:
                return None
        except Exception as e:
            raise Exception(f"Error fetching user by email: {str(e)}")
