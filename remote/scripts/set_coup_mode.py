from happygarden.mycoup import Coup
import sys

modes = {
    'mode_all_on':  """{"Coup": {"Lights": {"Run Light 1": true , "Run Light 2": true , "Coup Light 1": true, "Coup Light 2": true}}}""",
    'mode_all_off': """{"Coup": {"Lights": {"Run Light 1": false, "Run Light 2": false, "Coup Light 1": false, "Coup Light 2": false}}}""",
    'mode_pre_bed': """{"Coup": {"Lights": {"Run Light 1": true , "Run Light 2": false, "Coup Light 1": false, "Coup Light 2": false}}}"""
}

mode = modes[sys.argv[1]]

coup = Coup()
status = coup.get_status()
print("Starting state: {0}\nSetting to:     {1}".format(coup.get_status(), mode))
coup.set_state(mode)
print("Final state:    {0}".format(coup.get_status()))