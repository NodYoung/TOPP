import logging
import numpy as np
import os, sys
sys.path.insert(0, os.path.join('..', 'src'))
from python import TOPPpy
from python import Trajectory
from python import Utilities


def save_topp_input(trajectorystring, constraintstring):
  with open('trajectory_string', 'w') as f:
    f.write(trajectorystring)
  with open('constraint_string', 'w') as f:
    f.write(constraintstring)

def load_topp_output():
  with open('profiles_list', 'r') as f:
    profiles_list = TOPPpy.ProfilesFromString(f.read())
  with open('switchpoints_list', 'r') as f:
    switchpoints_list = TOPPpy.SwitchPointsFromString(f.read())
  with open('result_trajectory', 'r') as f:
    traj1 = Trajectory.PiecewisePolynomialTrajectory.FromString(f.read())
  return profiles_list, switchpoints_list, traj1

# reference: [Kinematic limits (initial trajectory specified by trajectorystring)](https://github.com/quangounet/TOPP/wiki/Quick-examples)
class QuickExample2(object):
  def __init__(self):
    ndof = 5
    trajectorystring = """1.0
    5
    -0.495010 1.748820 -2.857899 1.965396
    0.008319 0.004494 1.357524 -1.289918
    -0.354081 1.801074 -1.820616 0.560944
    0.221734 -1.320792 3.297177 -2.669786
    -0.137741 0.105246 0.118968 -0.051712
    1.0
    5
    0.361307 1.929207 -4.349490 2.275776
    0.080419 -1.150212 2.511645 -1.835906
    0.187321 -0.157326 -0.355785 0.111770
    -0.471667 -2.735793 7.490559 -4.501124
    0.034761 0.188049 -1.298730 1.553443"""
    self.traj0 = Trajectory.PiecewisePolynomialTrajectory.FromString(trajectorystring)
    # Constraints
    self.vmax = 2*np.ones(ndof)  # Velocity limits
    self.amax = 10*np.ones(ndof) # Acceleration limits

  def save_traj_constrain(self):
    trajectorystring = str(self.traj0)
    discrtimestep = 0.01
    constraintstring = str(discrtimestep)
    constraintstring += "\n" + ' '.join([str(v) for v in self.vmax])
    constraintstring += TOPPpy.ComputeKinematicConstraints(self.traj0, self.amax, discrtimestep)
    save_topp_input(trajectorystring, constraintstring)
  
  def plot_topp_res(self):
    profiles_list, switchpoints_list, traj1 = load_topp_output()
    TOPPpy.PlotProfiles(profiles_list, switchpoints_list, 4)
    dtplot = 0.01
    TOPPpy.PlotKinematics(self.traj0, traj1, dtplot, self.vmax, self.amax)

