def logic_engine_extension(sys_dict):
    """
    Refactored Logic Engine Extension to safely handle [SSD_I/O_FLUSH]
    events without causing a host lag timeout.
    """
    output = []
    for key, value in sys_dict.items():
        if key == 'SSD_I/O_FLUSH':
            for opt, data in enumerate(value):
                if isinstance(data, dict) and data.get('ID', 0) != 0:
                    output.append('SSD_IOPS_RESTRICTED')
        elif isinstance(value, dict) and (value.get('id', 0) < 0 or value.get('id', 0) > 100):
            output.append('You cannot enter a number greater than the ID of the system!')
            
    return output
