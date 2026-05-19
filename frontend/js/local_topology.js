window.LOCAL_TOPOLOGY = {
    "districts": [
        {
            "x": -35,
            "y": -25,
            "type": "CPU_CORE",
            "label": "LOCAL_CPU",
            "mid": "LCL",
            "settings": {
                "load": "0.00%",
                "temp": "N/A"
            }
        },
        {
            "x": -33,
            "y": -25,
            "type": "DIMM",
            "label": "LOCAL_RAM",
            "mid": "LCL",
            "settings": {
                "cap": "3.5 GB",
                "used": "93.6%"
            }
        },
        {
            "x": -35,
            "y": -23,
            "type": "NVME",
            "label": "LOCAL_SSD",
            "mid": "LCL",
            "settings": {
                "size": "118.18 GB",
                "fill": "76.3%"
            }
        },
        {
            "x": -38,
            "y": -25,
            "type": "SYS32",
            "label": "SYS32_BIN",
            "mid": "LCL"
        },
        {
            "x": -38,
            "y": -23,
            "type": "REG_HIVE",
            "label": "LOCAL_REG",
            "mid": "LCL"
        },
        {
            "x": -35,
            "y": -28,
            "type": "PROG_FILES",
            "label": "APPLICATIONS",
            "mid": "LCL"
        },
        {
            "x": -33,
            "y": -28,
            "type": "DOCS",
            "label": "USER_DOCS",
            "mid": "LCL"
        },
        {
            "x": -30,
            "y": -25,
            "type": "MODEM_HW",
            "label": "LOCAL_GW",
            "mid": "LCL"
        },
        {
            "x": 35,
            "y": -25,
            "type": "CPU_CORE",
            "label": "REMOTE_CPU",
            "mid": "RMT",
            "settings": {
                "cores": 8
            }
        },
        {
            "x": 37,
            "y": -25,
            "type": "DIMM",
            "label": "REMOTE_RAM",
            "mid": "RMT",
            "settings": {
                "cap": "8GB"
            }
        },
        {
            "x": 38,
            "y": -27,
            "type": "SYS32",
            "label": "RMT_SYS32",
            "mid": "RMT"
        },
        {
            "x": 30,
            "y": -25,
            "type": "MODEM_HW",
            "label": "REMOTE_GW",
            "mid": "RMT"
        },
        {
            "x": 0,
            "y": 35,
            "type": "ANDROID_NODE",
            "label": "PHONE_CLI",
            "mid": "PHN",
            "settings": {
                "ram": "4GB"
            }
        },
        {
            "x": -2,
            "y": 35,
            "type": "MODEM_HW",
            "label": "PHONE_LINK",
            "mid": "PHN"
        },
        {
            "x": 0,
            "y": 0,
            "type": "SRV_CLUSTER",
            "label": "HQ_CORE",
            "mid": "HQ"
        },
        {
            "x": 2,
            "y": 0,
            "type": "DATABASE",
            "label": "GLOBAL_LEDGER",
            "mid": "HQ"
        },
        {
            "x": 0,
            "y": -45,
            "type": "DATABASE",
            "label": "AWS_CLUSTER_01",
            "mid": "CLD",
            "skyscraper": true
        },
        {
            "x": 5,
            "y": -45,
            "type": "DATABASE",
            "label": "GCP_CLUSTER_01",
            "mid": "CLD",
            "skyscraper": true
        },
        {
            "x": -5,
            "y": -45,
            "type": "SRV_CLUSTER",
            "label": "AZURE_SPIRE",
            "mid": "CLD",
            "skyscraper": true
        }
    ],
    "agents": [
        {
            "x": -35,
            "y": -25,
            "name": "LCL_KERNEL",
            "role": "ADMIN",
            "stability": 100
        },
        {
            "x": -38,
            "y": -25,
            "name": "SYS_SENTRY",
            "role": "Bouncer",
            "stability": 100
        },
        {
            "x": 0,
            "y": 0,
            "name": "HQ_SI",
            "role": "SI",
            "stability": 100
        },
        {
            "x": 35,
            "y": -25,
            "name": "RMT_WATCHER",
            "role": "RAM Watcher",
            "stability": 100
        }
    ]
};