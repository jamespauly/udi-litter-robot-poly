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

        self.Notices = Custom(polyglot, 'notices')
        self.Parameters = Custom(polyglot, 'customparams')
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
        self.Notices.clear()
        self.Parameters.load(params)

        userValid = False
        passwordValid = False

        if self.Parameters['username'] is not None and len(self.Parameters['username']) > 0:
            userValid = True
        else:
            LOGGER.error('username is Blank')
        if self.Parameters['password'] is not None and len(self.Parameters['password']) > 0:
            passwordValid = True
        else:
            LOGGER.error('password is Blank')

        self.Notices.clear()

        if userValid and passwordValid:
            self.discover()

    def start(self):
        LOGGER.info('Staring LitterRobot NodeServer')
        self.poly.updateProfile()
        self.poly.setCustomParamsDoc()

    def query(self, command=None):
        LOGGER.info("Query sensor {}".format(self.address))
        self.discover()

    async def discover(self, *args, **kwargs):
        LOGGER.info("Starting LitterRobot Device Discovery")
        account = Account()

        try:
            # Connect to the API and load robots.
            await account.connect(username=self.Parameters['username'], password=self.Parameters['password'],
                                  load_robots=True)

            self.custom_data.load(account.session.tokens, True)

            for robot in account.robots:
                if isinstance(robot, LitterRobot4):
                    if self.poly.getNode(robot.serial) is None:
                        LOGGER.info(f'Adding Node {robot.serial} - {robot.name}')
                        self.poly.addNode(LitterRobot4Node(self.poly, self.address, robot.serial, robot.name, robot))
                        self.wait_for_node_event()
                    else:
                        LitterRobot_node = self.poly.getNode(robot.serial)
                        LitterRobot_node.query()
                        LOGGER.info(f'Node {robot.serial} - {robot.names} already exists, skipping')
        finally:
            await account.disconnect()

    LOGGER.info('Finished Node discovery')

    def delete(self):
        LOGGER.info('Deleting LitterRobot Node Server')

    def stop(self):
        LOGGER.info('LitterRobot NodeServer stopped.')

    id = 'litterrobot'
    commands = {
        'DISCOVER': discover
    }

    drivers = [
        {'driver': 'ST', 'value': 1, 'uom': 2}
    ]
