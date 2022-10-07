import os
import json
import logging
import matplotlib.pyplot as plt

PLOT_COLOR=['r', 'g', 'b', 'y', 'c', 'm', 'k']

def read_json_file(file_path):
  if not os.path.exists(file_path):
    raise ValueError("json file doesn't exist.")
  content = None
  with open(file_path, 'r') as f:
    content = json.load(f)
  return content

def plot_phase_plane():
  pass



if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO, format="%(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
  s_discr = read_json_file('discrsvect.json')
  sdt_mvc = read_json_file('mvcbobrow.json')  # maximum velocity curve
  sdt_mvc_combined = read_json_file('mvccombined.json')
  switchpoints = read_json_file('switchpointslist.json')
  result_profile = read_json_file('resprofileslist.json')
  zlajpah_points = read_json_file('zlajpahlist.json')
  sdata = dict(list(s_discr.items())+list(sdt_mvc.items())+list(sdt_mvc_combined.items())+list(switchpoints.items())
            +list(result_profile.items())+list(zlajpah_points.items()))
  plt.figure()
  # plt.plot(sdata['discrsvect'], sdata['mvcbobrow'], color=PLOT_COLOR[0], linewidth=1, marker='o', markersize=2, label='mvcbobrow')
  # plt.plot(sdata['discrsvect'], sdata['mvccombined'], color=PLOT_COLOR[1], linewidth=1, marker='o', markersize=2, label='mvccombined')
  plt.plot(sdata['discrsvect'], sdata['mvcbobrow'], color=PLOT_COLOR[0], linewidth=1, marker='', markersize=2, label='mvcbobrow')
  plt.plot(sdata['discrsvect'], sdata['mvccombined'], color=PLOT_COLOR[1], linewidth=1, marker='', markersize=2, label='mvccombined')
  label_first = [True, True, True, True]
  for p in sdata['switchpointslist']:
    if p['switchpointtype'] == 0:
      plt.plot(p['s'], p['sd'], 'ro', markersize=8, label='SP_TANGENT' if label_first[0] else '')
      label_first[0] = False
    if p['switchpointtype'] == 1:
      plt.plot(p['s'], p['sd'], 'go', markersize=8, label='SP_SINGULAR' if label_first[1] else '')
      label_first[1] = False
    if p['switchpointtype'] == 2:
      plt.plot(p['s'], p['sd'], 'bo', markersize=8, label='SP_DISCONTINUOUS' if label_first[2] else '')
      label_first[2] = False
    if p['switchpointtype'] == 3:
      plt.plot(p['s'], p['sd'], 'yo', markersize=8, label='SP_ZLAJPAH' if label_first[3] else '')
      label_first[3] = False
  label_first = True
  for profile in sdata['resprofileslist']:
    if profile['forward']:
      plt.plot(profile['svect'], profile['sdvect'], PLOT_COLOR[2], label='resprofileslist' if label_first else '')
    else:
      plt.plot(profile['svect'], profile['sdvect'], PLOT_COLOR[2], linestyle='--', label='resprofileslist' if label_first else '')
    label_first = False
  label_first = True
  for p in sdata['zlajpahlist']:
    plt.plot(p['s'], p['sd'], 'r*', markersize=8, label='zlajpahlist' if label_first else '')
    label_first = False
  plt.plot([8.85387, 5.39316, 0.257651], [2.53433, 3.18736, 2.30149], 'g*', markersize=8, label='sdcombined < sdcur <= sdbobrow')
  plt.ylim(0, 10)
  plt.title('Maximum Velocity Curves and profiles', fontsize=18)
  plt.xlabel('$s$', fontsize=18)
  plt.ylabel('$\dot s$', fontsize=18)
  plt.legend()
  # plt.show()
  plt.savefig('data_plot.png')