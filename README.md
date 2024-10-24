# fmo-tool
FMO-os system management tool

# Table of Contents
1. [Install auto-completion](#Install-auto-completion)
2. [FMO-TOOL modules](#fmo-tool-modules)
3. [Docker Compose Infrastructure (DCI) module](#Docker-Compose-Infrastructure-DCI-module)
   - [Check if DCI enabled for VM](#Check-if-DCI-enabled-for-VM)
   - [Check DCI service status for VM](#Check-DCI-service-status-for-VM)
   - [Start, stop or restart DCI service for VM](#Start-stop-or-restart-DCI-service-for-VM)
4. [Dynamic Devices Passthrough (DDP) module](#Dynamic-Devices-Passthrough-DDP-module)
   - [Check if DDP enabled for VM](#Check-if-DDP-enabled-for-VM)
   - [Enable / disable DDP for VM](#Enable-disable-DDP-for-VM)
   - [Print DDP config for VM](#Print-DDP-config-for-VM)
   - [Delete DDP rule for VM](#Delete-DDP-rule-for-VM)
   - [Add DDP rule for VM](#Add-DDP-rule-for-VM)
5. [Dynamic PortForwarding (DPF) module](#Dynamic-PortForwarding-DPF-module)
   - [Check if DPF enabled for VM](#Check-if-DPF-enabled-for-VM)
   - [Print DPF rules for VM](#Print-DPF-rules-for-VM)
   - [Delete DPF rule for VM](#Delete-DPF-rule-for-VM)
   - [Add DPF rule for VM](#Add-DPF-rule-for-VM)
   - [Check DPF status service status for VM](#Check-dpf-status-service-status-for-vm)
6. [VMs manage module](#VMs-manage-module)
7. [System manage module](#System-manage-module)
   - [Get system IP address](#Get-system-IP-address)
   - [Get system name](#Get-system-name)
   - [Get system release](#Get-system-release)
   - [Get system RA version](#Get-system-RA-version)
   - [Restore default system config](#Restore-default-system-config)

### Install auto-completion
In order to use auto-completion (use `TAB`) run following command:
```bash
$ fmo-tool --install-completion
bash completion installed in /home/$USER/.bash_completions/fmo-tool.sh
Completion will take effect once you restart the terminal
```

### FMO-TOOL modules
Currently `fmo-tool` contains following modules:
- `dci` - Docker Compose Infrastructure (DCI) module
- `ddp` - Dynamic Devices Passthrough (DDP) module
- `dpf` - Dynamic PortForwarding (DPF) module
- `ssh` - ssh to VMs module
- `vms` - VMs manage module
- `system` - System manage module

```bash
$ fmo-tool --help

 Usage: fmo-tool [OPTIONS] COMMAND [ARGS]...                                                                                                                               

╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                                                                                 │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.                                                          │
│ --help                        Show this message and exit.                                                                                                               │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ dci      Manage Docker Compose Infrastructure (DCI)                                                                                                                     │
│ ddp      Manage Dynamic Devices Passthrough (DDP)                                                                                                                       │
│ dpf      Manage Dynamic PortForwarding (DPF)                                                                                                                            │
│ ssh      SSH to vm                                                                                                                                                      │
│ system   Manage system                                                                                                                                                  │
│ vms      Manage VMs                                                                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### Docker Compose Infrastructure (DCI) module
Manage Docker Compose Infrastructure:
```bash
$ fmo-tool dci --help

 Usage: fmo-tool dci [OPTIONS] COMMAND [ARGS]...                                                                                                                           

 Manage Docker Compose Infrastructure (DCI)                                                                                                                                

╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                                             │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ enabled   Check DCI enabled status for VM                                                                                                                               │
│ restart   Request DCI restart                                                                                                                                           │
│ start     Request DCI start                                                                                                                                             │
│ status    Request DCI status                                                                                                                                            │
│ stop      Request DCI stop                                                                                                                                              │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

#### Check if DCI enabled for VM
```bash
$ fmo-tool dci enabled dockervm
True

$ fmo-tool dci enabled netvm
False
```

#### Check DCI service status for VM
```bash
$ sudo fmo-tool dci status dockervm
● fmo-dci.service
     Loaded: loaded (/etc/systemd/system/fmo-dci.service; enabled; preset: enabled)
     Active: activating (auto-restart) (Result: exit-code) since Thu 2024-10-24 08:13:05 UTC; 11s ago
    Process: 4934 ExecStart=/nix/store/f5iwvhsai8pds33a8rbw4awi796xwwlf-unit-script-fmo-dci-start/bin/fmo-dci-start (code=exited, status=14)
   Main PID: 4934 (code=exited, status=14)
         IP: 0B in, 0B out
        CPU: 54ms
```

#### Start, stop or restart DCI service for VM
```bash
sudo fmo-tool dci { start | stop | restart } dockervm
```

### Dynamic Devices Passthrough (DDP) module
```bash
$ fmo-tool ddp --help

 Usage: fmo-tool ddp [OPTIONS] COMMAND [ARGS]...                                                                                                                           

 Manage Dynamic Devices Passthrough (DDP)                                                                                                                                  

╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                                             │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ add        Add a new VM DDP rule                                                                                                                                        │
│ config     Print VM DDP config                                                                                                                                          │
│ delete     Delete the VM DDP rule                                                                                                                                       │
│ enabled    Check or set/reset DDP enabled status for VM                                                                                                                 │
│ generate   Generate VM DDP config                                                                                                                                       │
│ rules      Print VM DDP rules                                                                                                                                           │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

#### Check if DDP enabled for VM
```bash
$ fmo-tool ddp enabled netvm
False

$ fmo-tool ddp enabled dockervm
True
```

#### Enable / disable DDP for VM
```bash
$ sudo fmo-tool ddp enabled -e dockervm
True

$ sudo fmo-tool ddp enabled -d netvm
False
```

#### Print DDP config for VM
```bash
$ fmo-tool ddp rules dockervm
0 {'bus': 'usb', 'productid': '01a9', 'vendorid': '1546'}
1 {'bus': 'usb', 'productid': '2303', 'vendorid': '067b'}
```

#### Delete DDP rule for VM
```bash
$ fmo-tool ddp rules dockervm
0 {'bus': 'usb', 'productid': '01a9', 'vendorid': '1546'}
1 {'bus': 'usb', 'productid': '2303', 'vendorid': '067b'}

$ sudo fmo-tool ddp delete dockervm 1
Delete rule: 1
Delete rule: {'bus': 'usb', 'productid': '2303', 'vendorid': '067b'}
Please unplug the device for rules to take effect!
```

#### Add DDP rule for VM
```bash
$ lsusb 
Bus 004 Device 005: ID 413c:81d7 Dell Inc. DW5821e Snapdragon X20 LTE
...
Bus 003 Device 004: ID 067b:2303 Prolific Technology Inc. USB-Serial Controller -- let's add this device
...
Bus 001 Device 001: ID 1d6b:0002 Linux 6.1.38 xhci-hcd xHCI Host Controller

$ sudo fmo-tool ddp add -v 067b -p 2303 dockervm
Add a new rule
```

### Dynamic PortForwarding (DPF) module
```bash
$ fmo-tool dpf --help

 Usage: fmo-tool dpf [OPTIONS] COMMAND [ARGS]...                                                                                                                           

 Manage Dynamic PortForwarding (DPF)                                                                                                                                       

╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                                             │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ add       Add a new VM DPF rule                                                                                                                                         │
│ config    Print VM DPF config                                                                                                                                           │
│ delete    Delete the VM DPF rule                                                                                                                                        │
│ enabled   Check or set/reset DPF enabled status for VM                                                                                                                  │
│ restart   Request DPF restart                                                                                                                                           │
│ rules     Print VM DPF rules                                                                                                                                            │
│ start     Request DPF start                                                                                                                                             │
│ status    Request DPF status                                                                                                                                            │
│ stop      Request DPF stop                                                                                                                                              │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

#### Check if DPF enabled for VM
```bash
$ fmo-tool dpf enabled netvm
True
$ fmo-tool dpf enabled dockervm
False
```

#### Print DPF rules for VM
```bash
$ fmo-tool dpf rules netvm
...
6 {'dip': '192.168.101.11', 'dport': '123', 'proto': 'udp', 'sport': '123', 'sip': 'NA'}
7 {'dip': '192.168.101.11', 'dport': '123', 'proto': 'tcp', 'sport': '123', 'sip': 'NA'}
8 {'dip': '192.168.101.2', 'dport': '22', 'proto': 'tcp', 'sport': '42', 'sip': 'NA'}
```

if you want to apply / play with those rules manually:
```bash
$ fmo-tool dpf rules netvm -v
...
iptables -I INPUT -p udp --dport 123 -j ACCEPT
iptables -t nat -I PREROUTING -p udp -d 192.168.101.11 --dport 123 -j DNAT --to-destination NA:123
iptables -I INPUT -p tcp --dport 123 -j ACCEPT
iptables -t nat -I PREROUTING -p tcp -d 192.168.101.11 --dport 123 -j DNAT --to-destination NA:123
iptables -I INPUT -p tcp --dport 42 -j ACCEPT
iptables -t nat -I PREROUTING -p tcp -d 192.168.101.2 --dport 42 -j DNAT --to-destination NA:22
```
*`NA` means IP address will be taken from ip-address file*

#### Delete DPF rule for VM
```bash
$ fmo-tool dpf rules netvm
...
6 {'dip': '192.168.101.11', 'dport': '123', 'proto': 'udp', 'sport': '123', 'sip': 'NA'}
7 {'dip': '192.168.101.11', 'dport': '123', 'proto': 'tcp', 'sport': '123', 'sip': 'NA'}
8 {'dip': '192.168.101.2', 'dport': '22', 'proto': 'tcp', 'sport': '42', 'sip': 'NA'}

$ sudo fmo-tool dpf delete netvm 8
Delete rule: 8
Delete rule: {'dip': '192.168.101.2', 'dport': '22', 'proto': 'tcp', 'sport': '42'}
```

#### Add DPF rule for VM
```bash
$ sudo fmo-tool dpf add --dip 192.168.101.11 --sport 42 --dport 22 netvm
Add a new rule

# To apply new rules need to restart DPF service:
$ sudo fmo-tool dpf restart netvm
```

#### Check DPF status service status for VM
```bash
$ sudo fmo-tool dpf status netvm
○ fmo-dynamic-portforwarding-service.service
     Loaded: loaded (/etc/systemd/system/fmo-dynamic-portforwarding-service.service; enabled; preset: enabled)
     Active: inactive (dead) since Thu 2024-10-24 08:38:04 UTC; 1min 12s ago
   Duration: 647ms
    Process: 1438 ExecStart=/nix/store/n5v2igzmi74s123q85v24hxfsr5z1lzb-unit-script-fmo-dynamic-portforwarding-service-start/bin/fmo-dynamic-portforwarding-service-start (code=exited, status=0/SUCCESS)
   Main PID: 1438 (code=exited, status=0/SUCCESS)
         IP: 0B in, 0B out
        CPU: 358ms

...
Oct 24 08:38:04 netvm fmo-dynamic-portforwarding-service-start[1438]: Apply a new port forwarding: 192.168.248.1:123 to 192.168.101.11:123 proto: udp
Oct 24 08:38:04 netvm fmo-dynamic-portforwarding-service-start[1438]: Apply a new port forwarding: 192.168.248.1:123 to 192.168.101.11:123 proto: tcp
Oct 24 08:38:04 netvm fmo-dynamic-portforwarding-service-start[1438]: Apply a new port forwarding: 192.168.248.1:42 to 192.168.101.11:22 proto: tcp
Oct 24 08:38:04 netvm systemd[1]: fmo-dynamic-portforwarding-service.service: Deactivated successfully.
```

#### Start, stop, restart DPF service for VM
```bash
sudo fmo-tool dpf { start | stop | restart } netvm
```

### ssh to VMs module
You can  ssh to VMs with only `sudo` password:
```bash
[host:~]$ sudo fmo-tool ssh netvm
Last login: Thu Oct 24 07:11:10 2024 from 192.168.zzz.xxx

[netvm:~]$ 
```

### VMs manage module
You may get VMs `list`, check VM `ip` address, `ssh` to vm, { `start` | `stop` | `restart` } VM and check it's status
```bash
$ sudo fmo-tool vms --help

 Usage: fmo-tool vms [OPTIONS] COMMAND [ARGS]...                                                                                                                           

 Manage VMs                                                                                                                                                                

╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                                             │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ config    Print VM config                                                                                                                                               │
│ ip        Get VM IP address                                                                                                                                             │
│ list      Get VM list                                                                                                                                                   │
│ restart   Restart VM                                                                                                                                                    │
│ ssh       SSH to vm                                                                                                                                                     │
│ start     Start VM                                                                                                                                                      │
│ status    Get VM status                                                                                                                                                 │
│ stop      Stop VM                                                                                                                                                       │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### System manage module
```bash
$ sudo fmo-tool system --help

 Usage: fmo-tool system [OPTIONS] COMMAND [ARGS]...                                                                                                                        

 Manage system                                                                                                                                                             

╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                                             │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ alias     Get/Set system alias                                                                                                                                          │
│ config    Get full system config                                                                                                                                        │
│ cr        Get/Set system docker Container Repository                                                                                                                    │
│ gw        Get/Set system default gateway                                                                                                                                │
│ ip        Get/Set system ip address                                                                                                                                     │
│ name      Get system iso name                                                                                                                                           │
│ ra        Get system RegistrationAgent version                                                                                                                          │
│ release   Get system release version                                                                                                                                    │
│ restore   Restore default config                                                                                                                                        │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

#### Get system IP address
```bash
$ fmo-tool system ip
192.168.248.1
```

#### Get system name
```bash
$ fmo-tool system name
fmo-os-rugged-laptop-7330
```

#### Get system release
```bash
$ fmo-tool system release
v1.0.0a
```

#### Get system RA version
```bash
$ fmo-tool system ra
v0.8.4
```

#### Restore default system config
```bash
$ sudo fmo-tool system restore
```
