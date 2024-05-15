import asyncio
import time

import udi_interface
from nodes import LitterRobot4Node
from pylitterbot import Account, LitterRobot4

# IF you want a different log format than the current default
LOGGER = udi_interface.LOGGER
Custom = udi_interface.Custom

class LitterRobotController(udi_interface.Node):
    def __init__(self, polyglot, primary, address, name):
        super(LitterRobotController, self).__init__(polyglot, primary, address, name)
        self.poly = polyglot
        self.name = name
        self.primary = primary
        self.address = address
        self.n_queue = []

        self.notices = Custom(polyglot, 'notices')
        self.parameters = Custom(polyglot, 'customparams')
        self.custom_data = Custom(polyglot, 'customdata')

        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.CUSTOMPARAMS, self.parameter_handler)
        self.poly.subscribe(self.poly.ADDNODEDONE, self.node_queue)

        self.poly.ready()
        self.poly.addNode(self)

    def node_queue(self, data):
        self.n_queue.append(data['address'])

    def wait_for_node_event(self):
        while len(self.n_queue) == 0:
            time.sleep(0.1)
        self.n_queue.pop()

    def parameter_handler(self, params):
        self.notices.clear()
        self.parameters.load(params)

        userValid = False
        passwordValid = False

        if self.parameters['username'] is not None and len(self.parameters['username']) > 0:
            userValid = True
        else:
            LOGGER.error('username is Blank')
        if self.parameters['password'] is not None and len(self.parameters['password']) > 0:
            passwordValid = True
        else:
            LOGGER.error('password is Blank')

        self.notices.clear()

        if userValid and passwordValid:
            asyncio.run(self.discover())

    def start(self):
        LOGGER.info('Starting LitterRobot NodeServer')
        self.poly.updateProfile()
        self.poly.setCustomParamsDoc()

    def query(self, command=None):
        LOGGER.info("Query sensor {}".format(self.address))
        asyncio.run(self.discover())

    async def discover(self, *args, **kwargs):
        LOGGER.info("Starting LitterRobot Device Discovery")
        account = Account()

        try:
            # Connect to the API and load robots.
            await account.connect(username=self.parameters['username'], password=self.parameters['password'],
                                  load_robots=True)

            self.custom_data.load(account.session.tokens, True)

            for robot in account.robots:
                if isinstance(robot, LitterRobot4):
                    node_address = self.poly.getValidAddress(robot.serial)
                    node_name = self.poly.getValidName(robot.name)
                    if self.poly.getNode(node_address) is None:
                        LOGGER.info(f'Adding Node {node_address} - {node_name}')
                        self.poly.addNode(LitterRobot4Node(self.poly, self.address, node_address, node_name, robot.id, self.parameters['username'], self.parameters['password']))
                        self.wait_for_node_event()
                    else:
                        LitterRobot_node = self.poly.getNode(node_address)
                        LitterRobot_node.query()
                        LOGGER.info(f'Node {node_address} - {node_name} already exists, skipping')
        finally:
            await account.disconnect()

    LOGGER.info('Finished Node discovery')

    def delete(self):
        LOGGER.info('Deleting LitterRobot Node Server')

    def stop(self):
        LOGGER.info('LitterRobot NodeServer stopped.')

    id = 'litterrobot'
    commands = {
        'DISCOVER': query
    }

    drivers = [
        {'driver': 'ST', 'value': 1, 'uom': 2}
    ]
