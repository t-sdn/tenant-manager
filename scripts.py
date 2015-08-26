import subprocess


def run_script(script):
    p = subprocess.Popen(
        ['sh'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    p.stdin.write(script)
    p.stdin.close()
    p.wait()
    stdout = p.stdout.read()
    stderr = p.stderr.read()

    return stdout, stderr


def make_tenant(name, ip, vni, interface):
    """
    Make tenant network

    :param name: tenant name.
    :param ip: IP address to network.
    :param vni: VNI number.
    :param interface: Make tenant network using this interface.
    """

    script = '\n'.join([
        'name={0}',
        'ip={1}',
        'vni={2}',
        'interface={3}',
        'sudo /sbin/ip netns add $name',
        'sudo /sbin/brctl addbr br_$name',
        'sudo /sbin/ip link set dev br_$name up',
        'sudo /sbin/ip link add veth0 type veth peer name veth0_$name ',
        'sudo /sbin/ip link set veth0 netns $name',
        'sudo /sbin/ip netns exec $name ip link set dev veth0 up',
        'sudo /sbin/ip netns exec $name ifconfig veth0 $ip '
        'netmask 255.255.255.0 up',
        'sudo /sbin/ip link set dev veth0_$name up',
        '#',
        '# Binding VNI $vni to br_$name',
        '# Binding veth0_$name to br_$name',
        '#',
        'sudo /sbin/ip link add vxlan_$vni type vxlan id $vni '
        'remote 10.10.10.133 local 10.10.10.139 dstport 4789 dev $interface',
        'sudo /sbin/ip link set dev vxlan_$vni up',
        'sudo /sbin/brctl addif br_$name veth0_$name',
        'sudo /sbin/brctl addif br_$name vxlan_$vni',
        '# Configuring mtu for $name and vxlan_$vni',
        'sudo /sbin/ifconfig vxlan_$vni mtu 1500',
        'sudo /sbin/ifconfig $interface mtu 9000',
    ]).format(name, ip, vni, interface)

    return run_script(script)
