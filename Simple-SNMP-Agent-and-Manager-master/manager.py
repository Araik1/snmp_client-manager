from pysnmp.hlapi import *
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902


def snmpGet(community, host, port, oid):
    errorIdication, errrorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                    CommunityData(community),
                    UdpTransportTarget((host, port)),
                    ContextData(),
                    ObjectType(ObjectIdentity(oid))
            ))

    if errorIdication:
        print(errorIdication)
    elif errrorStatus:
        print('%s at %s' % (errrorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            print(' = '.join([x.prettyPrint() for x in varBind]))


def snmpSet(community, host, port, oid, newVar):
    errorIdication, errrorStatus, errorIndex, varBinds = next(
        setCmd(SnmpEngine(),
                CommunityData(community),
                UdpTransportTarget((host, port)),
                ContextData(),
                (oid, rfc1902.OctetString(newVar)) )
        )

    if errorIdication:
        print(errorIdication)
    elif errrorStatus:
        print('%s at %s' % (errrorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            print(' = '.join([x.prettyPrint() for x in varBind]))


if __name__ == '__main__':
    try:
        print("Example request:\n\t snmpget community host port oid\n\t snmpset community host port oid newvar\n")
        while(True):
            strComand = input()
            if len(strComand) > 0:
                strComand = strComand.split()
                if strComand[0] == "snmpget":
                    print("Getting Objects:\n")
                    snmpGet(strComand[1], strComand[2], strComand[3], strComand[4])
                elif strComand[0] == "snmpset":
                    print("Setting Objects:\n")
                    snmpSet(strComand[1], strComand[2], strComand[3], strComand[4], strComand[5])
                else:
                    print("Input error try again")
                    print("Example request: snmpget community host port oid")
                    continue
            else:
                print("Input error try again")
                print("Example request: snmpget community host port oid")
                continue

    except KeyboardInterrupt:
        print("exit")
