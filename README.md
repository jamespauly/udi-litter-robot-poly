# Litter Robot Devices

This is a node server to interface with Daikin Mini-Split HVAC systems and make it available to a Universal Devices ISY994i Polyglot interface with Polyglot V3 running on a Polisy

### Currently, supports Litter Robot 4

#### Installation

1. Backup Your ISY!
2. Go to the Polyglot Store in the UI and install.
3. From the Polyglot dashboard, select the Litter Robot node server.
3. Restart the Admin Console to properly display the new node server nodes.

#### Configuration
1. No configuration needed.  Tt will autodetect and set them up automatically if they are on the same network as the Litter Robot.
2. You can enter in a broadcast IP of another network by using the following custom param:
   1. <b>broadcast_ips (Optional)</b> - Broadcast IP addresses of networks.  You can enter multiple by use a comma delimiter. ex. (192.168.1.255,192.168.2.255)
      1. https://www.calculator.net/ip-subnet-calculator.html

#### Requirements

Here is what is required to use this poly:<BR>
[pylitterbot](https://github.com/natekspencer/pylitterbot)
<BR>https://github.com/natekspencer/pylitterbot
