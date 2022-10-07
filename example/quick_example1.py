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

# reference: [Kinematic limits (initial trajectory specified by via-points)](https://github.com/quangounet/TOPP/wiki/Quick-examples)
class QuickExample1(object):
  def __init__(self):
    # A two-dof path going through 5 viapoints (0,1) - (1,1) - (5,1) - (3,2) - (5,4)
    path = np.array([[0,1,5,3,5],[1,1,1,2,4]])
    self.traj0 = Utilities.InterpolateViapoints(path) # Interpolate using splines
    # Constraints
    self.vmax = 2*np.ones(self.traj0.dimension)  # Velocity limits
    logging.info('vmax={}'.format(self.vmax))
    self.amax = 10*np.ones(self.traj0.dimension) # Acceleration limits
    self.profiles_list = None
    self.switchpoints_list = None
    self.traj1 = None

  def save_traj_constrain(self):
    trajectorystring = str(self.traj0)
    discrtimestep = 0.005
    constraintstring = str(discrtimestep)
    constraintstring += "\n" + ' '.join([str(v) for v in self.vmax])
    constraintstring += TOPPpy.ComputeKinematicConstraints(self.traj0, self.amax, discrtimestep)
    # logging.info('ComputeKinematicConstraintsJson={}'.format(TOPPpy.ComputeKinematicConstraintsJson(self.traj0, self.vmax, self.amax, discrtimestep)))
    save_topp_input(trajectorystring, constraintstring)
  
  def plot_topp_result(self):
    profiles_list, switchpoints_list, traj1 = load_topp_output()
    TOPPpy.PlotProfiles(profiles_list, switchpoints_list, 4)
    dtplot = 0.01
    TOPPpy.PlotKinematics(self.traj0, traj1, dtplot, self.vmax, self.amax)


if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO, format="%(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
  qe1 = QuickExample1()
  qe1.save_traj_constrain()
  # qe1.plot_topp_result()

  
