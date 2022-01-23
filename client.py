from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport


class OxidQL:

    def __init__(self, **kwargs):
        self.headers = {}
        self.client = self.get_client()
        self.authorize(**kwargs)

    def get_client(self):
        transport = AIOHTTPTransport(url="http://65.21.146.137/ox/source/graphql/", headers=self.headers)
        client = Client(transport=transport, fetch_schema_from_transport=True)
        return client

    def authorize(self, **kwargs):

        if kwargs.get('token'):
            self.headers = {'Authorization': 'Bearer ' + kwargs['token']}
        else:
            assert all([kwargs.get('username'), kwargs.get('password')]), "token or username and password required"
            credentials = f"""token (
                                username: '{kwargs['username']}',
                                password: '{kwargs['password']}'
                        )"""
            query = "query {" + credentials + "}"
            result = await self.client.execute_async(gql(query))
            self.headers = {'Authorization': 'Bearer ' + result['token']}