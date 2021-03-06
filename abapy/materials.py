'''
Materials
=========
'''

def float_arg(arg):
  """
  Tests if an arg is float or convertible to float
  """
  try:
    arg = [float(arg)]
  except:
    pass
  return arg    
  

class VonMises(object):
  ''' 
  Represents von Mises materials used for FEM simulations
  
  :param E: Young's modulus.
  :type E: float, list, array.array
  :param nu: Poisson's ratio.
  :type nu: float, list, array.array
  :param sy: Yield stress.
  :type sy: float, list, array.array
  
  .. note:: 
     All inputs must have the same length or an exception will be raised.
     
     
  >>> from abapy.materials import VonMises
  >>> m = VonMises(labels='myMaterial',E=1,nu=0.45, sy=0.01)
  >>> print m.dump2inp()
  ...
  
  
  '''
  def __init__(self, labels='mat', E = 1., nu = 0.3, sy = 0.01, dtf='d'):
    from array import array
    import numpy
    if type(labels) is str: labels=[labels]
    self.labels=labels
    l = len(labels)
    E = float_arg(E)
    if len(E) != l: raise Exception, 'Parameters must all have the same length'
    self.E=array(dtf,E)
    nu = float_arg(nu)
    if len(nu) != l: raise Exception, 'Parameters must all have the same length'
    self.nu=array(dtf,nu)  
    sy = float_arg(sy)
    if len(sy) != l: raise Exception, 'Parameters must all have the same length'
    self.sy=array(dtf,sy)
  def __repr__(self):
    return '<VonMises instance: {0} samples>'.format(len(self.E))
  def dump2inp(self):
    '''
    Returns materials in INP format suitable with abaqus input files.
    
    :rtype: string
    '''
    out = '** {0}\n'.format(self.__repr__())
    pattern = '*MATERIAL, NAME={0}\n*ELASTIC\n  {1}, {2}\n*PLASTIC\n  {3}, 0.\n'
    for i in xrange(len(self.E)):
      out += pattern.format(self.labels[i],self.E[i],self.nu[i],self.sy[i])
    return out[0:-1]

class Elastic(object):
  ''' 
  Represents an istotrop linear elastic material used for FEM simulations
  
  :param E: Young's modulus.
  :type E: float, list, array.array
  :param nu: Poisson's ratio.
  :type nu: float, list, array.array
  
  .. note:: 
     All inputs must have the same length or an exception will be raised.
  '''
  def __init__(self, labels='mat', E = 1., nu = 0.3, dtf='d'):
    from array import array
    if type(labels) is str: labels=[labels]
    self.labels=labels
    l = len(labels)
    E = float_arg(E)
    if len(E) != l: raise Exception, 'Parameters must all have the same length'
    self.E=array(dtf,E)
    nu = float_arg(nu)
    if len(nu) != l: raise Exception, 'Parameters must all have the same length'
    self.nu=array(dtf,nu)  
  def __repr__(self):
    return '<Elastic instance: {0} samples>'.format(len(self.E))
  def dump2inp(self):
    '''
    Returns materials in INP format suitable with abaqus input files.
    
    :rtype: string
    '''
    out = '** {0}\n'.format(self.__repr__())
    pattern = '*MATERIAL, NAME={0}\n*ELASTIC\n  {1}, {2}\n'
    for i in xrange(len(self.E)):
      out += pattern.format(self.labels[i],self.E[i],self.nu[i])
    return out[0:-1]


class DruckerPrager(object):
  ''' 
  Represents Drucker-Prager materials used for FEM simulations
  
  :param E: Young's modulus.
  :type E: float, list, array.array
  :param nu: Poisson's ratio.
  :type nu: float, list, array.array
  :param sy: Compressive yield stress.
  :type sy: float, list, array.array
  :param beta: Friction angle in degrees.
  :type beta: float, list, array.array
  :param psi: Dilatation angle in degress. If psi = beta, the plastic flow is associated. If psi = None, the associated flow is automatically be chosen.
  :type psi: float, list, array.array or None
  :param k: tension vs. compression asymmetry. For k = 1., not asymmetry, for k=0.778 maximum possible asymmetry.
  :type k: float, list, array.array
  
  .. note:: 
     All inputs must have the same length or an exception will be raised.
     
   ...
  
  
  '''
  def __init__(self, labels='mat', E = 1., nu = 0.3, sy = 0.01, beta = 10., psi = None, k = 1., dtf='d'):
    from array import array
    if type(labels) is str: labels=[labels]
    self.labels=labels
    l = len(labels)
    E = float_arg(E)
    if len(E) != l: raise Exception, 'Parameters must all have the same length'
    self.E=array(dtf,E)
    nu = float_arg(nu)
    if len(nu) != l: raise Exception, 'Parameters must all have the same length'
    self.nu=array(dtf,nu)  
    sy = float_arg(sy)
    if len(sy) != l: raise Exception, 'Parameters must all have the same length'
    self.sy=array(dtf,sy)
    beta = float_arg(beta)
    if len(beta) != l: raise Exception, 'Parameters must all have the same length'
    self.beta = array(dtf,beta)
    if psi == None: psi = beta
    psi = float_arg(psi)
    if len(psi) != l: raise Exception, 'Parameters must all have the same length'
    self.psi = array(dtf,psi)
    k = float_arg(k)
    if len(k) != l: raise Exception, 'Parameters must all have the same length'
    self.k = array(dtf,k)
  
  def __repr__(self):
    return '<DruckerPrager instance: {0} samples>'.format(len(self.E))
  
  def dump2inp(self):
    '''
    Returns materials in INP format suitable with abaqus input files.
    
    :rtype: string
    '''
    out = '** {0}\n'.format(self.__repr__())
    pattern = '*MATERIAL, NAME={0}\n*ELASTIC\n  {1}, {2}\n*DRUCKER PRAGER\n  {3}, {4}, {5}\n*DRUCKER PRAGER HARDENING\n  {6}, 0.\n'
    for i in xrange(len(self.E)):
      out += pattern.format(
        self.labels[i],
        self.E[i],
        self.nu[i],
        self.beta[i],
        self.k[i],
        self.psi[i],
        self.sy[i])
    return out[0:-1]
    
class Hollomon(object):
  ''' 
  Represents von Hollom materials (i. e. power law haderning and von mises yield criterion) used for FEM simulations.
  
  :param E: Young's modulus.
  :type E: float, list, array.array
  :param nu: Poisson's ratio.
  :type nu: float, list, array.array
  :param sy: Yield stress.
  :type sy: float, list, array.array
  :param n: hardening exponent
  :type sy: float, list, array.array
  
  .. note:: 
     All inputs must have the same length or an exception will be raised.
    
  .. plot:: example_code/materials/Hollomon.py
    :include-source:   
  
  
  '''
  def __init__(self, labels='mat', E = 1., nu = 0.3, sy = 0.01, n = 0.2, dtf='d'):
    from array import array
    import numpy
    if type(labels) is str: labels=[labels]
    self.labels=labels
    l = len(labels)
    E = float_arg(E)
    if len(E) != l: raise Exception, 'Parameters must all have the same length'
    self.E=array(dtf,E)
    nu = float_arg(nu)
    if len(nu) != l: raise Exception, 'Parameters must all have the same length'
    self.nu=array(dtf,nu)  
    sy = float_arg(sy)
    if len(sy) != l: raise Exception, 'Parameters must all have the same length'
    self.sy=array(dtf,sy)
    n = float_arg(n)
    if len(n) != l: raise Exception, 'Parameters must all have the same length'
    self.n=array(dtf,n)
  def __repr__(self):
    return '<Hollomon instance: {0} samples>'.format(len(self.E))
  
  def get_table(self, position, eps_max = 10., N = 100):
    '''
    Returns the tabular data corresponding to the tensile stress strain law using log spacing.
    
    :param eps_max: maximum strain to be computed.
    :type eps_max: float
    :param N: number of points to be computed.
    :type N: int
    :rtype: ``numpy.array``
    '''
    import numpy as np
    sy = self.sy[position]
    E = self.E[position]
    n = self.n[position]
    ey = sy/E
    s = 10.**np.linspace(0., np.log10(eps_max/ey), N, endpoint = True)
    eps = ey * s
    sigma = sy * s**n
    return np.array([eps, sigma]).transpose()
      
  def dump2inp(self, eps_max = 10., N = 100):
    '''
    Returns materials in INP format suitable with abaqus input files.
    
    :param eps_max: maximum strain to be computed.
    :type eps_max: float
    :param N: number of points to be computed.
    :type N: int
    :rtype: string
    '''
    out = '** {0}\n'.format(self.__repr__())
    pattern = '*MATERIAL, NAME={0}\n*ELASTIC\n  {1}, {2}\n*PLASTIC\n{3}\n'
    for i in xrange(len(self.E)):
      table = self.get_table(position = i, eps_max = eps_max, N = N)
      sigma = table[:,1]
      eps = table[:,0]
      #eps_p = eps - eps[0]
      eps_p = [eps[j] - sigma[j] / self.E[i] for j in xrange(len(eps))]
      data = ''
      for j in xrange(len(table)):
        data += '  {0}, {1}\n'.format(sigma[j], eps_p[j])
      out += pattern.format(self.labels[i],self.E[i],self.nu[i],data[0:-1])
    return out[0:-1]
    
    
    
class Bilinear(object):
  ''' 
  Represents von Mises materials used for FEM simulations
  
  :param E: Young's modulus.
  :type E: float, list, array.array
  :param nu: Poisson's ratio.
  :type nu: float, list, array.array
  :param Ssat: Saturation stress.
  :type Ssat: float, list, array.array
  :param n: Slope of the first linear plastic law
  :type n: float, list, array.array
  :param Sy: Stress at zero plastic strain
  :type Sy: float, list, array.array
  
  .. note:: 
     All inputs must have the same length or an exception will be raised.
     
  '''
  def __init__(self, labels='mat', E = 1., nu = 0.3, Ssat = 1000., n=100., sy=100. ,dtf='d'):
    from array import array
    import numpy
    
    if type(labels) is str: labels=[labels]
    self.labels=labels
    l = len(labels)
    E = float_arg(E)
    if len(E) != l: raise Exception, 'Parameters must all have the same length'
    self.E=array(dtf,E)
    nu = float_arg(nu)
    if len(nu) != l: raise Exception, 'Parameters must all have the same length'
    self.nu=array(dtf,nu)  
    Ssat = float_arg(Ssat)
    if len(Ssat) != l: raise Exception, 'Parameters must all have the same length'
    self.Ssat=array(dtf,Ssat)
    n = float_arg(n)
    if len(n) != l: raise Exception, 'Parameters must all have the same length'
    self.n=array(dtf,n)
    sy = float_arg(sy)
    if len(sy) != l: raise Exception, 'Parameters must all have the same length'
    self.sy=array(dtf,sy)    
    
  def __repr__(self):
    return '<Bilinear instance: {0} samples>'.format(len(self.E))
  
  def dump2inp(self):
    '''
    Returns materials in INP format suitable with abaqus input files.
    
    :rtype: string
    '''
    out = '** {0}\n'.format(self.__repr__())
    pattern = '*MATERIAL, NAME={0}\n*ELASTIC\n  {1}, {2}\n*PLASTIC\n  {3}, 0.\n {4}, {5}'
    Eps_p_sat=[]
    for i in xrange(len(self.E)):
      Eps_p_sat.append((self.Ssat[i] - self.sy[i])/self.n[i])
      out += pattern.format(self.labels[i],self.E[i],self.nu[i],self.sy[i], self.Ssat[i], Eps_p_sat[i])
    return out[0:-1]    
