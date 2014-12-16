#!/usr/bin/env python
# dominfo - print some information about a domain

import libvirt
import sys
import os
import libxml2

def usage():
   print 'Usage: %s HYPERVISOR-URI SERVER-NAME ' % sys.argv[0]
   print '       Print information about the domain(s) on HYPERVISOR'

def print_entry(key, value):
    print "%-10s %-10s" % (key, value)

def get_xml_value(key, ctx, path):
    res = ctx.xpathEval(path)
    if res is None or len(res) == 0:
        value="Unknown"
    else:
        value = res[0].content
    return value

def get_vol_size(conn, storage, vol):
    try:
       size = conn.storagePoolLookupByName(storage)\
               .storageVolLookupByName(vol).info()[2] / (1024*1024*1024)
       return "%s" % size
    except libvirt.libvirtError:
        print "%s" % storage
        return "-1"

def list_vm_info(hypervisor):
    # Connect to libvirt
    conn = libvirt.openReadOnly(hypervisor)
    if conn == None:
        print 'Failed to open connection to the hypervisor'
        sys.exit(1)
    host      = conn.getHostname()
    host_info = conn.getInfo()
    pool_info = conn.listStoragePools() 
    vol_dict  = dict([(vol,
                      (strp,
                       get_vol_size(conn, strp, vol)
                      )
                     ) for strp in conn.listStoragePools() 
                       for vol in conn.storagePoolLookupByName(strp).listVolumes()
                       if strp != "iso" ])
    dom_data  = dict([])

    try:
        for dom in [conn.lookupByName(name) for name in conn.listDefinedDomains()]\
                        + [conn.lookupByID(vmid) for vmid in conn.listDomainsID()]:
            dom_info = {}
            info = dom.info()

            # Read some info from the XML desc
            xmldesc = dom.XMLDesc(0)
            doc = libxml2.parseDoc(xmldesc)
            ctx = doc.xpathNewContext()
            #section  Devices  
            devs = ctx.xpathEval("/domain/devices/*")
            volsize = 0
            for d in devs:
                ctx.setContextNode(d)
                disktype = get_xml_value("Type:", ctx, "@type")
                if disktype in ["file", "block"]:
                    if disktype == "file":
                        src = get_xml_value("Source:", ctx, "source/@file")
                    else:
                        src = get_xml_value("Source:", ctx, "source/@dev")
                    #dst = get_xml_value("Target:", ctx, "target/@dev")
                    if src.endswith(".iso") or src in ["Unknown", "None"]:
                        next
                    else:
                        if os.path.basename(src) not in vol_dict.keys():
                            continue
                        if len(vol_dict.get(os.path.basename(src), ("",""))) > 1:
                            volsize += float(vol_dict.get(os.path.basename(src), ("",""))[1])
            dom_info = { 
                    "hypervisor":   host,
                    "dom_name":     dom.name(),
                    "used_memory":  str(info[2]/1024),
                    "max_memory":   str(info[1]/1024),
                    "vcpus":        str(info[3]),
                    "state":        "up" if info[0] == 1 else "down",
                    "volsize":      volsize,
                    }

            dom_data[dom.name()] = dom_info

        # value for hypervisor
        capacity   = 0
        allocation = 0
        available  = 0
        for sto in [conn.storagePoolLookupByName(name) for name in conn.listStoragePools()]:
            if sto.name() not in [ 'iso' ]:
                capacity   += int(sto.info()[1]) / (1000**3)
                allocation += int(sto.info()[2]) / (1000**3)
                available  += int(sto.info()[3]) / (1000**3)

        d0_poolinfo = {
                "capacity":   capacity,
                "allocation": allocation,
                "available":  available,
                }

        dom_data[host] =  { 
                    "hypervisor":   host,
                    "dom_name":     host,
                    "used_memory":  str(host_info[1]),
                    "max_memory":   str(host_info[1]),
                    "vcpus":        "0",
                    "state":        "",
                    "volsize":      d0_poolinfo,
                    }
        return dom_data
        # Annoyiingly, libvirt prints its own error message here
    except libvirt.libvirtError:
        print "Domain %s is not runing" % name
        sys.exit(0)
