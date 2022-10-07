

class QuickExample3(object):
  def __init__(self):
    trajstr = """0.500000
      3
      0.0 0.0 -35.9066153846 47.930797594
      0.0 0.0 -0.645566686001 1.11351913336
      0.0 0.0 8.3609538376 -11.3580450529
      0.500000
      3
      0.0 0.1 -0.159247917034 0.0789972227119
      0.0 0.1 -32.7720979649 43.5627972865
      0.0 0.1 0.958473557774 -1.41129807703"""
    self.traj0 = Trajectory.PiecewisePolynomialTrajectory.FromString(trajstr)
    self.vmax = np.ones(3)
    self.accelmax = np.ones(3)

  def save_traj_constrain(self):
    trajectorystring = str(self.traj0)
    inertia = np.eye(3)
    discrtimestep = 1e-3
    constraintstring = str(discrtimestep)
    constraintstring += "\n" + ' '.join([str(a) for a in self.accelmax])
    for v in inertia:
      constraintstring += "\n" + ' '.join([str(i) for i in v])
    save_topp_input(trajectorystring, constraintstring)