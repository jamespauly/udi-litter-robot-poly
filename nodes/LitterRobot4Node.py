import asyncio

import udi_interface
from pylitterbot import Account
from pylitterbot.robot.litterrobot4 import NightLightMode, BrightnessLevel

from enums.LitterRobot4Status import LitterRobot4Status
from enums.LitterRobot4GlobeStatus import LitterRobot4GlobeStatus

LOGGER = udi_interface.LOGGER
Custom = udi_interface.Custom

loop = asyncio.get_event_loop()


class LitterRobot4Node(udi_interface.Node):
    def __init__(self, polyglot, primary, address, name, robot_id, username, password):
        super(LitterRobot4Node, self).__init__(polyglot, primary, address, name)

        self.username = username
        self.password = password
        self.robot_id = robot_id
        self.tokens = {}

        self.custom_data = Custom(polyglot, 'customdata')

        self.poly.subscribe(self.poly.CUSTOMDATA, self.custom_data_handler)
        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.POLL, self.poll)

    def custom_data_handler(self, data):
        LOGGER.info("Entering custom_data_handler")
        self.custom_data.load(data)
        self.tokens['id_token'] = self.custom_data['id_token']
        self.tokens['refresh_token'] = self.custom_data['refresh_token']
        LOGGER.info("Exiting custom_data_handler")

    async def update(self):
        LOGGER.info("Updating LitterRobot Device")
        account = Account(token=self.tokens)
        try:
            # Connect to the API and load robots.
            # await account.connect(username=self.username, password=self.password,
            #                       load_robots=True)
            await account.load_robots()
            updated_robot = account.get_robot(self.robot_id)
            # updated_robot = next(filter(lambda x: x.serial.lower() == self.address, account.robots))

            self.setDriver('GV0', updated_robot.litter_level, True)
            self.setDriver('GV1', updated_robot.waste_drawer_level, True)
            self.setDriver('GV2', updated_robot.cycle_count, True)
            self.setDriver('GV3', LitterRobot4Status(updated_robot.status_code).index, True)
            self.setDriver('GV4', LitterRobot4GlobeStatus(updated_robot.night_light_mode.value).index, True)
            self.setDriver('GV5', updated_robot.night_light_brightness, True)
            self.setDriver('GV6', updated_robot.panel_brightness.value, True)
            self.setDriver('GV7', updated_robot.panel_lock_enabled, True)
            self.setDriver('GV8', updated_robot.clean_cycle_wait_time_minutes, True)
            self.reportDrivers()

        finally:
            await account.disconnect()

    LOGGER.info('Finished Updating LitterRobot Device')

    async def set_globe_light_power(self, status):
        LOGGER.info("Entering set_globe_light_power")
        LOGGER.info(f'status: {status["value"]}')
        account = Account(token=self.tokens)
        i_status = int(status["value"])
        try:
            await account.load_robots()
            updated_robot = account.get_robot(self.robot_id)
            if (i_status == 0):
                await updated_robot.set_night_light_mode(NightLightMode.OFF)
            elif (i_status == 1):
                await updated_robot.set_night_light_mode(NightLightMode.ON)
            elif (i_status == 2):
                await updated_robot.set_night_light_mode(NightLightMode.AUTO)
        finally:
            await account.disconnect()

        self.setDriver('GV4', i_status, True)

    async def set_globe_light_brightness(self, status):
        LOGGER.info("Entering set_globe_light_brightness")
        LOGGER.info(f'status: {status["value"]}')
        account = Account(token=self.tokens)
        i_status = int(status["value"])
        try:
            await account.load_robots()
            updated_robot = account.get_robot(self.robot_id)
            if (i_status == 25):
                await updated_robot.set_night_light_brightness(BrightnessLevel.LOW)
            elif (i_status == 50):
                await updated_robot.set_night_light_brightness(BrightnessLevel.MEDIUM)
            elif (i_status == 100):
                await updated_robot.set_night_light_brightness(BrightnessLevel.HIGH)
        finally:
            await account.disconnect()

        self.setDriver('GV5', i_status, True)

    async def set_panel_brightness(self, status):
        LOGGER.info("Entering set_panel_brightness")
        LOGGER.info(f'status: {status["value"]}')
        account = Account(token=self.tokens)
        i_status = int(status["value"])
        try:
            await account.load_robots()
            updated_robot = account.get_robot(self.robot_id)
            if (i_status == 25):
                await updated_robot.set_panel_brightness(BrightnessLevel.LOW)
            elif (i_status == 50):
                await updated_robot.set_panel_brightness(BrightnessLevel.MEDIUM)
            elif (i_status == 100):
                await updated_robot.set_panel_brightness(BrightnessLevel.HIGH)
        finally:
            await account.disconnect()

        self.setDriver('GV6', i_status, True)

    async def set_litter_box_wait_time(self, wait_time):
        LOGGER.info("Entering set_litter_box_wait_time")
        LOGGER.info(f'status: {wait_time["value"]}')
        account = Account(token=self.tokens)
        i_wait_time = int(wait_time["value"])
        try:
            await account.load_robots()
            updated_robot = account.get_robot(self.robot_id)
            await updated_robot.set_wait_time(i_wait_time)
        finally:
            await account.disconnect()

        self.setDriver('GV8', i_wait_time, True)

    def cmd_globe_light(self, cmd):
        loop.run_until_complete(self.set_globe_light_power(cmd))

    def cmd_globe_light_brightness(self, cmd):
        loop.run_until_complete(self.set_globe_light_brightness(cmd))

    def cmd_panel_brightness(self, cmd):
        loop.run_until_complete(self.set_panel_brightness(cmd))

    def cmd_litter_box_wait_time(self, cmd):
        loop.run_until_complete(self.set_litter_box_wait_time(cmd))

    def poll(self, pollType):
        if 'shortPoll' in pollType:
            LOGGER.info('shortPoll (node)')
            self.query()

    def query(self):
        LOGGER.info("Query sensor {}".format(self.address))
        # asyncio.run(self.update())
        loop.run_until_complete(self.update())

    def start(self):
        LOGGER.info("Starting {}".format(self.address))
        self.query()

    drivers = [{'driver': 'GV0', 'value': 0, 'uom': '51'},  # Litter Level
               {'driver': 'GV1', 'value': 0, 'uom': '51'},  # Waste Level
               {'driver': 'GV2', 'value': 0, 'uom': '0'},  # Scoops Saved
               {'driver': 'GV3', 'value': 0, 'uom': '25'},  # Robot Status
               {'driver': 'GV4', 'value': 2, 'uom': '25'},  # Globe Light
               {'driver': 'GV5', 'value': 50, 'uom': '25'},  # Globe Brightness
               {'driver': 'GV6', 'value': 25, 'uom': '25'},  # Panel Brightness
               {'driver': 'GV7', 'value': 0, 'uom': '2'},  # Panel Locked
               {'driver': 'GV8', 'value': 7, 'uom': '45'}  # Litter Box Wait Time
               ]

    commands = {
        'QUERY': query,
        'GLOBE_LIGHT_MODE': cmd_globe_light,
        'GLOBE_LIGHT_BRIGHT': cmd_globe_light_brightness,
        'LITTER_BOX_WAIT_TIME': cmd_litter_box_wait_time,
        'PANEL_LIGHT_BRIGHT': cmd_panel_brightness
    }

    id = 'lrnode4'
