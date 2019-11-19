from pysnmp.entity import engine, config
from pysnmp import debug
from pysnmp.entity.rfc3413 import cmdrsp, context, ntforg
from pysnmp.carrier.asynsock.dgram import udp
from pysnmp.smi import builder


def createVariable(SuperClass, getValue, setValue, *args):
    class Var(SuperClass):
        def readGet(self, name, *args):
        	print( "Getting obj")
        	return name, self.syntax.clone(getValue())

        def writeCommit(self, name, val, *args ):
        	print ("Setting obj...")
        	setValue(val)

    return Var(*args)


class SNMPAgent(object):

    def __init__(self, host, port, mibObjects):
        self._snmpEngine = engine.SnmpEngine()

        config.addSocketTransport(self._snmpEngine, udp.domainName,
                                  udp.UdpTransport().openServerMode((host, port)))

        config.addV1System(self._snmpEngine, "agent", "publick")# password
        config.addV1System(self._snmpEngine, 'my-write-area', 'private')
        
        config.addVacmUser(self._snmpEngine, 2, "agent", "noAuthNoPriv",
                           readSubTree=(1,3,6,1,4,1))

        config.addVacmUser(self._snmpEngine, 2, 'my-write-area', 'noAuthNoPriv', 
            readSubTree=(1, 3, 6, 1, 4, 1), writeSubTree=(1, 3, 6, 1, 4, 1))

        self._snmpContext = context.SnmpContext(self._snmpEngine)

        mibBuilder = self._snmpContext.getMibInstrum().getMibBuilder()
        mibSources = mibBuilder.getMibSources() + (builder.DirMibSource('.'),)
        mibBuilder.setMibSources(*mibSources)
        
        MibScalarInstance, = mibBuilder.importSymbols('SNMPv2-SMI',
                                                      'MibScalarInstance')
        for mibObject in mibObjects:
            nextVar, = mibBuilder.importSymbols(mibObject.mibName,
                                                mibObject.objectType)
            instance = createVariable(MibScalarInstance,
                                      mibObject.valueFunc,
                                      mibObject.valueSetFunc,
                                      nextVar.name, (0,),
                                      nextVar.syntax)

            instanceDict = {str(nextVar.name)+"Instance":instance}
            mibBuilder.exportSymbols(mibObject.mibName,
                                     **instanceDict)

        cmdrsp.GetCommandResponder(self._snmpEngine, self._snmpContext)
        cmdrsp.SetCommandResponder(self._snmpEngine,self._snmpContext)
        cmdrsp.NextCommandResponder(self._snmpEngine, self._snmpContext)
        cmdrsp.BulkCommandResponder(self._snmpEngine, self._snmpContext)

    def serve_forever(self):
        print ("Starting agent...")
        self._snmpEngine.transportDispatcher.jobStarted(1)
        try:
           self._snmpEngine.transportDispatcher.runDispatcher()
        except:
            self._snmpEngine.transportDispatcher.closeDispatcher()
            raise
