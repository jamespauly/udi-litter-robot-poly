class LitterBot:
    def __init__(self, username, password, tokens):

    def login(self):
        account = Account()
        try:
            # Connect to the API and load robots.
            await account.connect(username=self.parameters['username'], password=self.parameters['password'],
                                  load_robots=True)

