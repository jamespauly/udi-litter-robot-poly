import asyncio

import udi_interface
from pylitterbot import Account
from enums.LitterRobot4Status import LitterRobot4Status

LOGGER = udi_interface.LOGGER


class LitterRobot4Node(udi_interface.Node):
    def __init__(self, polyglot, primary, address, name, robot):
        super(LitterRobot4Node, self).__init__(polyglot, primary, address, name)

        self.robot = robot

        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.POLL, self.poll)

    async def update(self):
        LOGGER.info("Updating LitterRobot Device")
        account = Account()

        try:
            # Connect to the API and load robots.
            await account.connect(username=self.Parameters['username'], password=self.Parameters['password'],
                                  load_robots=True)

            self.custom_data.load(account.session.tokens, True)

            updated_robot = next(filter(lambda x: x.serial == self.robot.serial, account.robots))

            self.poly.setDriver('GV0', updated_robot.litter_level, True)
            self.poly.setDriver('GV1', updated_robot.waste_drawer_level, True)
            self.poly.setDriver('GV2', updated_robot.cycle_count, True)
            self.poly.setDriver('GV3', LitterRobot4Status(updated_robot.status_code).index, True)

        finally:
            await account.disconnect()

    LOGGER.info('Finished Updating LitterRobot Device')

    def poll(self, pollType):
        if 'shortPoll' in pollType:
            LOGGER.info('shortPoll (node)')
            self.query()

    def query(self):
        LOGGER.info("Query sensor {}".format(self.address))
        asyncio.run(self.update())

    def start(self):
        self.query()

    drivers = [{'driver': 'GV0', 'value': 0, 'uom': '51'},  # Litter Level
               {'driver': 'GV1', 'value': 0, 'uom': '51'},  # Waste Level
               {'driver': 'GV2', 'value': 0, 'uom': '0'},  # Scoops Saved
               {'driver': 'GV3', 'value': 0, 'uom': '25'}  # Robot Status
               ]

    commands = {
        'QUERY': query
    }

    id = 'litterrobot4node'
