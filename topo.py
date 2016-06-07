from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def emptyNet():

    "Create an empty network and add nodes to it."

    net = Mininet( controller=None )

    info( '*** Adding controller\n' )

    net.addController( 'c0', controller=RemoteController, ip='192.168.142.50', port=6633 )

    info( '*** Adding hosts\n' )

    h1 = net.addHost( 'h1', ip='10.0.0.101', mac='00:00:00:00:00:01' )

    h2 = net.addHost( 'h2', ip='10.0.0.102', mac='00:00:00:00:00:02' )

    h3 = net.addHost( 'h3', ip='10.0.0.103', mac='00:00:00:00:00:03' )

    h4 = net.addHost( 'h4', ip='10.0.0.104', mac='00:00:00:00:00:04' )

    info( '*** Adding switch\n' )

    s1 = net.addSwitch( 's1', protocols='OpenFlow13' )

    s2 = net.addSwitch( 's2', protocols='OpenFlow13' )

    s3 = net.addSwitch( 's3', protocols='OpenFlow13' )   

    info( '*** Creating links\n' )

    net.addLink( h1, s1 )

    net.addLink( h2, s1 )

    net.addLink( h3, s3 )

    net.addLink( h4, s3 )

    net.addLink( s1, s2 )

    net.addLink( s2, s3 )

    info( '*** Starting network\n')

    net.start()

    info( '*** Running CLI\n' )

    CLI( net )

    info( '*** Stopping network' )

    net.stop()

if __name__ == '__main__':

    setLogLevel( 'info' )

    emptyNet()
