import sys
import niscope as ni
import datetime
sys.path.insert(1, r'C:\\Users\\oper\\SynologyDrive\\Lab2023\\KIDs\\QTLab2324\\IRSource\\PXIe5170R\\')
from ..PXIe5170R import DAQ

def get_date(file_name = None):
    now = datetime.now()
    date= now.strftime("%d%m%y")
    hour = now.strftime("%H%M%S")
    name = file_name + '_' + date + '_' + hour
    return (date, hour) if file_name == None else name


def main():
    device = 'PXI1Slot3'
    scheda = DAQ.DAQ(device)

    vertical = {
        'range': 1,
        'coupling': ni.VerticalCoupling.DC,
        'offset': 0.0,
        'probe_attenuation': 0.0,
        'enabled': True
    }

    chan_char = {
        'input_impedance': float(50), #(50 Ohms?)
        'max_input_frequency': float()
    }

    horizontal = {
        'min_sample_rate': 5e7,
        'min_num_pts': 1000,
        'ref_position': float(),
        'num_records': 10000,
        'enforce_realtime': True
    }

    trigger = {
        'trigger_type'    : 'DIG',
        'trigger_source'  : '1',
        'level'           : '-0.031',
        'trigger_coupling': None,
        'slope'           : ni.TriggerSlope.POSITIVE,
        'holdoff'         : 0.0,
        'delay'           : 0.0       
    }

    trigger_edge = {
            'trigger_type'    : 'EDGE',
            'trigger_source': '',
            'level': 2,
            'trigger_coupling': ni.enums.TriggerCoupling.AC,
            'slope': ni.TriggerSlope.POSITIVE,
            'holdoff' : 0.0,
            'delay' : 0.0
        }
    
    scheda.vertical_conf(vertical)
    scheda.vertical_dic
    scheda.test()
    scheda.session_reset()
    scheda.device_reset()
    scheda.reset_with_def()
    scheda.get_status()
    scheda.available
    scheda.commit()
    scheda.initiate()
    scheda.chan_conf(chan_char)
    scheda.horizontal_conf(horizontal)
    scheda.config_vertical()
    scheda.config_hor_timing()
    scheda.config_chan_char()
    scheda.set_trigger_dic(trigger_edge)
    scheda.config_edge_trigger()
    scheda.set_trigger_dic(trigger)
    scheda.config_dig_trigger()
    scheda.get_trigger_type
    scheda.config_software_trigger()
    scheda.available
    scheda.logger.info('END EXECUTION\n\n')