from mib import Mib
from snmpagent import SNMPAgent
import collections
import time

MibObject = collections.namedtuple('MibObject', ['mibName',
                                   'objectType', 'valueFunc','valueSetFunc'])

if __name__ == '__main__':
    mib = Mib()
    objects = [MibObject('MY-MIB', 'platform', mib.getPlatform, mib.setPlatform),
               MibObject('MY-MIB', 'platformRelease', mib.getPlatformRelease, mib.setPlatformRelease),
               MibObject('MY-MIB', 'platformVersion', mib.getPlatformVersion, mib.setPlatformVersion),
               MibObject('MY-MIB', 'architecture', mib.getArchitecture, mib.setArchitecture),
               MibObject('MY-MIB', 'hostname', mib.getHostname, mib.setHostname),
               MibObject('MY-MIB', 'ipAddress', mib.getIpAddress, mib.setIpAddress),
               MibObject('MY-MIB', 'macAddress', mib.getMacAddress, mib.setMacAddress),
               MibObject('MY-MIB', 'processor', mib.getProcessor, mib.setProcessor),
               MibObject('MY-MIB', 'ram', mib.getRam, mib.setRam),
               ]
    agent = SNMPAgent('127.0.0.1', 171, objects)
    
    try:
        agent.serve_forever()
    except KeyboardInterrupt:
        print ("Shutting down")