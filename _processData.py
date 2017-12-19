"""
this library contains a number of useful functions that are general purpose 
data processing functions.
"""

### import common libraries
import numpy as _np
import matplotlib.pyplot as _plt
import copy as _copy
import _plotDataTools as _pdt
import math as _math

            
    
def find_nearest(array,value):
    """
    search through array and returns the index of the cell closest to the 
    value.
    
    Parameters
    ----------
    array : numpy.array
        data array to search through
    value : float (or int)
        value to look for in array
        
    Return
    ------
    idx : int
        index of value in array that is closest to value
    
    References
    ----------
    http://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array
    """
    idx = (_np.abs(array-value)).argmin()
    return idx #array[idx] #index instead of value
    
    
def rmse(data, targets=0):
    """
    Root mean square error function.  
    If targets = 0, this is also the root mean square function.  
    
    Parameters
    ----------
    data : numpy.array 
        Data being considered
    target : numpy.array of floats
        values being compared against
        
    Return
    ------
    root mean square error
    
    References
    ----------
    # http://stackoverflow.com/questions/17197492/root-mean-square-error-in-python
    # http://statweb.stanford.edu/~susan/courses/s60/split/node60.html
    """
    return _np.sqrt(((data - targets) ** 2).mean())
    
    
def rms(data):
    """
    Root mean square function.   
    
    Parameters
    ----------
    data : numpy.array 
        Data being considered
        
    Return
    ------
    root mean square 
    
    References
    ----------
    # http://stackoverflow.com/questions/17197492/root-mean-square-error-in-python
    # http://statweb.stanford.edu/~susan/courses/s60/split/node60.html
    """
    return _np.sqrt(((data - 0) ** 2).mean())
    
    
def rejectOutliers(data, m=2):
    """
    remove outliers from set of data
    
    Parameters
    ----------
    data : numpy.ndarray
        data array being considered
    m : int
        the number of std. devs. about which to reject data.  E.g. m=2 rejects 
        outliers outside of +-2*sigma
        
    Return
    ------
    Data array as above but missing entires considered as outliers
    
    References
    ----------
    http://stackoverflow.com/questions/11686720/is-there-a-numpy-builtin-to-reject-outliers-from-a-list
    """
    return data[abs(data - _np.mean(data)) < m * _np.std(data)]
                
      
def boxCar(data,c=25):
    """
    box car smoothing algorithm.  home brew.
    
    Parameters
    ----------
    data : numpy.ndarray
        data being smoothed
    c : int
        plus and minus number of points to include in box car.  I.e. c=25 means
        that the function is smoothing over 51 points
        
    Return
    ------
    sData : numpy.ndarray
        smoothed data array
        
    Notes
    -----
    TODO(John) Check indices.  I'm not 100% this function works EXACTLY as 
    stated above.  
    
    """
    n=len(data);
    sData=_np.zeros(n);
    for i in range(0,n):
        if i < c:  # left edge
            sData[i]=_np.sum(data[0:i+c])/(i+c)
        elif i > n-c:  # right edge
            sData[i]=_np.sum(data[i-c:n])/(n-i+c+1)            
        else:
            sData[i]=_np.sum(data[i-c:i+c+1])/(2.*c+1)
    return sData
                
                
def wrapPhase(data): 
    """
    Wraps phase data so that it repeats every 2pi.
    This is important for phase data when you want it to all fit nicely on a 
    plot.  
    
    Parameters
    ----------
    data : numpy.ndarray
        data being wrapped
        
    Return
    ------
    outData : numpy.ndarray
        wrapped data array
        
    """
    inData=_copy.copy(data);
    outData=_np.zeros(inData.size);
    inData-=_np.pi;
    for i in range(0,_np.size(inData)-1):
        a=_np.floor(inData[i]/(_np.pi*2))
        outData[i]=inData[i]-(a+1)*2*_np.pi+_np.pi
    return outData
    
    
def unwrapPhase(inData):
    """
    Takes in phase array (in radians).  I think it needs to be centered about 0.
    Unwraps phase data so that it is continuous.
    This is important for phase data when you want to take it's derivative to
    get frequency.  
    
    Parameters
    ----------
    data : numpy.ndarray
        data being unwrapped
        
    Return
    ------
    outData : numpy.ndarray
        unwrapped data array
        
    """
    outData=_np.zeros(_np.size(inData));
    offset=0;
    outData[0]=inData[0];
    for i in range(0,_np.size(inData)-1):
        if inData[i] > _np.pi/4 and inData[i+1] < -_np.pi/4:
            offset=offset+2*_np.pi;
        elif inData[i] < -_np.pi/4 and inData[i+1] > _np.pi/4:
            offset=offset-2*_np.pi;
        outData[i+1]=inData[i+1]+offset;
    return outData


def hasNan(inArray):
    """
    searches input array, inArray, for any occurances of NaN.  returns True if
    yes, returns False if no.
    
    Parameters
    ----------
    inArray : numpy.ndarray
        data array being considered for NaN entries
        
    Return
    ------
        : bool
        True if NaNs are in array, False otherwise
    """
    count = 0;
    for i in range(0,len(inArray)):
        if _math.isnan(inArray[i]):
            count+=1;
            
    print "There was/were %d instances of NaN" % count
    
    if count == 0:
        return False
    if count != 0:
        return True
        
        
def sort2Arrays(array1, array2):
    """
    sorts array1 and array2 in ascending order of array1
    
    outdated:  replaced by sortArrays() below
    """
    array1, array2 = zip(*sorted(zip(array1, array2)));
    array1=_np.array(array1);
    array2=_np.array(array2);
    return array1, array2
    
    
def sortArrays(arrays,sortIndex):
    """
    sorts a list of n arrays.  sortIndex is the index of the array to sort all arrays.
    
    example use:  [V, I, phi]=sortArrays([V,I,phi],1) to sort all arrays by ascending I
    
    reference:  https://stackoverflow.com/questions/6618515/sorting-list-based-on-values-from-another-list
    """
    sortedIndices=arrays[sortIndex].argsort()
    for i in range(len(arrays)):
        arrays[i]=arrays[i][sortedIndices]
    return arrays
    
    
def downSampleData(downX,data,xIndex=0):
    """
    Down samples data by finding the nearest x values on data that match the downselecting x (downX)
    
    downX = the pre-down selected x array
    data = list of arrays to be down sized
    xIndex = index of data array to be compared against downX
    """
    m=len(downX)
    indices=_np.zeros(m,dtype=_np.int16)
    out = []
    
    for i in range(0,m):
        indices[i]=int(find_nearest(data[xIndex],downX[i]))

    for i in range(0,len(data)):
        out.append(data[i][indices])
    return out
    
    
def upSampleData(upX,downX,data):
    """
    Up samples data by linear interpolating 
    
    upX = the x-data that we are sampling up to
    downX = the x-data that we are sampling from
    data = single array of data associated with downX
    """
    return _np.interp(upX,downX,data)
    

    
    
def linearizeDataMatrix(data):
    """
    data is assumed to be a list of arrays
    
    this function converts the data to a single, appended array
    """
    m=len(data);
    temp=_np.array([])
    for i in range(0,m):
        temp=_np.append(temp,data[i])
    return temp
    
    
    
###############################################################################
### fitting functions and related
    
class polyFitData:
    """ 
    Polynomial fit function.  
    
    Parameters
    ----------
    yData : 'numpy.array'
        dependent variable
    xData : 'numpy.array'
        independent variable
    order : int
        order of polynomial fit.  1 = linear, 2 = quadratic, etc.
    plot : bool
        Causes a plot of the fit to be generated

    Attributes
    ----------
    coefs : 'numpy.array'
        array of fit coefficients, starts at highest order.  
    ffit : 'numpy.lib.polynomial.poly1d'
        function that returns yFit data given ANY numpy.array of x values
    fitData : 'numpy.array'
        yFit data corresponding to xData
    plotOfFit : 
        custom plot class of data. 
        
    Notes
    -----
    This is merely a wrapper function for the numpy.polyfit function.  However,
    it also plots the result automatically.  
    
    output:
    fitData is the y fit data.   
    """
    
    def __init__(self, yData, xData,order=2, plot=True):
        title = str(order)+' order Polynomial fit'
    
        ### do fit
        self.coefs=_np.polyfit(xData, yData, order)
        self.ffit = _np.poly1d(self.coefs)
        self.fitData=self.ffit(xData)
        
        ### generate plot        
        self.plotOfFit=_pdt.prePlot();
        self.plotOfFit.xLabel='x'
        self.plotOfFit.yLabel='y'
        self.plotOfFit.title=title;
        
        ### raw data
        self.plotOfFit.xData.append(xData)
        self.plotOfFit.yData.append(yData)
        self.plotOfFit.marker.append('.')
        self.plotOfFit.linestyle.append('')
        self.plotOfFit.alpha.append(.15)
        self.plotOfFit.yLegendLabel.append('raw data')
        
        ### fit
        x=_np.linspace(_np.min(xData),_np.max(xData),1000);
        self.plotOfFit.xData.append(x)
        self.plotOfFit.yData.append(self.ffit(x))
        self.plotOfFit.marker.append('')
        self.plotOfFit.linestyle.append('-')
        self.plotOfFit.alpha.append(1.)
        self.plotOfFit.yLegendLabel.append('poly fit order %d'%order)
        
        if plot==True:
            self.plotOfFit.plot()
            
    
class genericCurveFit:
    """
    generic curve fitting function that uses scipy.optimize.curve_fit solution
    
    I "think" I like the genericLeastSquaresFit code better than this function.  See below.
    
    func = fit function
    indepVars = independent variables.  for multivariable, use indepVars = (x,y) etc.
    depVars = dependent variable.  this is the single dependent variable that we are trying to model
    guess = guess parameters.  use: guess = 8., 2., 7. etc.  
    
    note:  this function CAN be upgraded to include bounds
    
    references:
        https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html
    
        #######################
        ## example usage
        
        def dumbModel(variables,a,b,c):
            x,y=variables
            return _np.log(a) + b*_np.log(x) + c*_np.log(y)
        
        # some artificially noisy data to fit
        x = _np.linspace(0.1,1.1,101)
        y = _np.linspace(1.,2., 101)
        a, b, c = 10., 4., 6.
        z = dumbModel((x,y), a, b, c) * 1 + _np.random.random(101) / 100
        
        # initial guesses for a,b,c:
        p0 = 8., 2., 7.
        
        # solve
        indepVars=(x,y)
        a=genericCurveFit(dumbModel, indepVars, z, p0)

    """    
    

    def __init__(self,func, indepVars,depVar,guess, bounds=None,plot=True , maxNumIterations = None, fileName=''):
        self.indepVars=indepVars;
        self.depVars=depVar
        self.fileName=fileName
        
        
        from scipy.optimize import curve_fit
    
        if bounds == None:
            self.fitParams,self.covMatrix = curve_fit(func, indepVars, depVar, guess) #, max_nfev = 1e2 , max_nfev=maxNumIterations
        else:
            self.fitParams,self.covMatrix = curve_fit(func, indepVars, depVar, guess, bounds=bounds) #, max_nfev = 1e2 , max_nfev=maxNumIterations
#        print self.fitParams
#        print self.covMatrix
        self.fitSoln=func(indepVars, *self.fitParams)
#        print fitSoln

        self.R2=rSquared(indepVars, self.fitSoln)
        print r"$R^2$ = %.3E" % self.R2

        if plot==True:
            self.plot();
    
    def plot(self):
        _plt.figure()
        _plt.plot(self.fitSoln, self.depVars, '.', label='scipy.optimize.curve_fit solution',alpha=0.10)
#        _plt.plot(self.solnRobust, self.depData, 'x', label='robust least squares soln')
        _plt.plot(_np.array([_np.min(self.depVars),_np.max(self.depVars)]),_np.array([_np.min(self.depVars),_np.max(self.depVars)]),color='r',linestyle='--',linewidth=5)
        _plt.xlabel('Fit Solution')
        _plt.ylabel('Dependent Data')
        _plt.legend()    
        _plt.grid()
#        alphaB, alphaV, alphaR, phi0, C, C2 = self.fitParams
        #        _plt.ylim([-5,30])
        _plt.axes().set_aspect('equal') #, 'datalim'
        if self.fileName != '':
            _plt.savefig(self.fileName+'.png')


def expFun(x, a,b,c):
    """
    Basic exponential function.
    Used primarily with fitting functions.  
    """
    return a*_np.exp(x/b)+c
    
    
# define sin cos function
def cosFunc(x, a,b,c,d):
    """
    Cosine function.
    Used primarily with fitting functions.  
    """
    return a*_np.cos(x*d*2*_np.pi+b)+c
    

def singlePowerTerm(x, a,b,c):
    """
    basic single power term
    """
    return a*(x)**b+c
    
    
class cosFit:
    """
    Cos fit function

    Parameters
    ----------
    y : numpy.ndarray
        dependent data
    x : numpy.ndarray
        independent array
    guess : list
        list of three floats.  these are the guess values.
    plot : bool
        causes the results to be plotted
        
    Attributes
    ----------
    fit : genericLeastSquaresFit
    
    Notes
    -----
    if you are receiving the error: "ValueError: Residuals are not finite in 
    the initial point.", most likely, you need to play with your initial 
    conditions to get them closer to the right answer before the fit will work
    correctly.  
    
    Example use
    -----------
    # import library first.  I set it as hbt.pd 
    
    >>> y=np.array([11.622967, 12.006081, 11.760928, 12.246830, 12.052126, 12.346154, 12.039262, 12.362163, 12.009269, 11.260743, 10.950483, 10.522091,  9.346292,  7.014578,  6.981853,  7.197708,  7.035624,  6.785289, 7.134426,  8.338514,  8.723832, 10.276473, 10.602792, 11.031908, 11.364901, 11.687638, 11.947783, 12.228909, 11.918379, 12.343574, 12.046851, 12.316508, 12.147746, 12.136446, 11.744371,  8.317413, 8.790837, 10.139807,  7.019035,  7.541484,  7.199672,  9.090377,  7.532161,  8.156842,  9.329572, 9.991522, 10.036448, 10.797905])
    >>> x=np.linspace(0,2*np.pi,48)
    >>> c=hbt.pd.cosFit(y,x,guess=[2,0,10,.3])
    # note that this example took me quite a bit of guessing with the guess 
    # values before everything fit correctly.

    """
    def __init__(self,y,x,guess,plot=True):
        self.fit=genericLeastSquaresFit(x=x,x0=guess,y=y, function=cosFunc,plot=plot)


class expFit:
    """
    Exponential fit function

    Parameters
    ----------
    y : numpy.ndarray
        dependent data
    x : numpy.ndarray
        independent array
    guess : list
        list of three floats.  these are the guess values.
    plot : bool
        causes the results to be plotted
        
    Attributes
    ----------
    fit : genericLeastSquaresFit
    
    Notes
    -----
    if you are receiving the error: "ValueError: Residuals are not finite in 
    the initial point.", most likely, you need to play with your initial 
    conditions to get them closer to the right answer before the fit will work
    correctly.  
    
    Example use
    -----------
    # import library first.  I set it as hbt.pd 
    >>> x = np.array([399.75, 989.25, 1578.75, 2168.25, 2757.75, 3347.25, 3936.75, 4526.25, 5115.75, 5705.25])
    >>> y = np.array([109,62,39,13,10,4,2,0,1,2])
    >>> hbt.pd.expFit(y,x,guess=[10,-100,1])

    """
    def __init__(self,y,x,guess=[1,1,1], plot=True):
        self.fit=genericLeastSquaresFit(x=x,x0=guess,y=y, function=expFun)
        
    
class genericLeastSquaresFit:
    """
    Least squares fitting function(class)
    This is a wrapper for scipy.optimize.least_squares
    
    Parameters
    ----------
    y : numpy.ndarray
        dependent data
    x : numpy.ndarray (multidimensional)
        independent array(s).  multiple ind. variables are supported.  
    x0 : list
        list of three floats.  these are the guess values
    function : 
    yTrue : (optional) numpy.ndarray 
        if you know what the actual fit should be, include it here, and it will
        plot alongside the other data.  useful for debugging.  
    plot : bool
        causes the results to be plotted
        
    Attributes
    ----------
    fitParams : numpy.ndarray
        array of fit parameters, in the same order as the guess
    plotOfFit :
    plotOfFitDep :
        custom plot function of fit data plotted against dependent data.  this 
        is important if there is more than 1 dependent data array.
    rSquared : float
        r^2 result of the fit
    res : 
        fit output from scipy.optimize.least_squares
    yFit : numpy.ndarray
        y-fit data that corresponds with the independent data
    
    Notes
    -----
    i've found that the guess values often NEED to be somewhat close to the 
    actual values for the solution to converge
    
    Examples use
    ------------
    # define expoential function
    def expFun(x, a,b,c):
        return a*_np.exp(x/b)+c
    
    # generate noisy exponential signal
    x1=_np.linspace(-1,1,100);
    a=_np.zeros(len(x1));
    b=_np.zeros(len(x1));
    c=_np.zeros(len(x1));
    for i in range(0,len(x1)):
        a[i]=(random.random()-0.5)/4. + 1.
        b[i]=(random.random()-0.5)/4. + 1.
        c[i]=(random.random()-0.5)/4. + 1.
    y1=1+_np.pi*_np.exp(x1/_np.sqrt(2)) # actual solution
    y2=1*a+_np.pi*b*_np.exp(x1/_np.sqrt(2)/c) # noisy solution
        
    # perform fit
    d=genericLeastSquaresFit(x1,[1,1,1],y2, expFun, y1)
    """           
    
    def __init__(self, x, x0, y, function,yTrue=[],plot=True ):

        def fit_fun(x0,x,y):
            return function(x, *x0) - y

        from scipy.optimize import least_squares
        
        self.res=least_squares(fit_fun, x0, args=[x,y])  #args=(y)
        self.yFit=function(x, *self.res.x) 
        self.fitParams=self.res.x;
        
        # calculate r^2
        self.rSquared=rSquared(y,self.yFit)
        
        ### plot of fit
        # only makes this plot if there is a single indep. variable. 
        if type(x) is _np.ndarray or len(x)==1:
            self.plotOfFit=_pdt.prePlot();
            self.plotOfFit.yLabel='y'
            self.plotOfFit.xLabel='x'
            self.plotOfFit.title=r'R$^2$ = %.5f' % self.rSquared
            
            if isinstance(x,list):
                x=x[0]
            self.plotOfFit.xData.append(x)
            self.plotOfFit.yData.append(y)
            self.plotOfFit.yLegendLabel.append('raw data')
            self.plotOfFit.marker.append('.')
            self.plotOfFit.linestyle.append('')
            self.plotOfFit.color.append('b')
            self.plotOfFit.alpha.append(0.3)
            
            self.plotOfFit.xData.append(x)
            self.plotOfFit.yData.append(self.yFit)
            self.plotOfFit.yLegendLabel.append('fit')
            self.plotOfFit.marker.append('')
            self.plotOfFit.linestyle.append('-')
            self.plotOfFit.color.append('r')
            self.plotOfFit.alpha.append(1.)
            
            if yTrue!=[]:
                self.plotOfFit.xData.append(x)
                self.plotOfFit.yData.append(yTrue)
                self.plotOfFit.yLegendLabel.append('True Soln')
                self.plotOfFit.marker.append('')
                self.plotOfFit.linestyle.append('-')
                self.plotOfFit.color.append('k')
                self.plotOfFit.alpha.append(1.)
                
        ### plot of fit vs dependent data.  important if there are multiple
        ###         independent variables.
        self.plotOfFitDep=_pdt.prePlot();
        self.plotOfFitDep.yLabel='fit data'
        self.plotOfFitDep.xLabel='raw data'
        self.plotOfFitDep.aspect="equal"
        
        self.plotOfFitDep.xData.append(y)
        self.plotOfFitDep.yData.append(self.yFit)
        self.plotOfFitDep.yLegendLabel.append('actual fit')
        self.plotOfFitDep.marker.append('.')
        self.plotOfFitDep.linestyle.append('')
        self.plotOfFitDep.color.append('b')
        self.plotOfFitDep.alpha.append(0.3)
        
        self.plotOfFitDep.xData.append(_np.array([_np.min(y),_np.max(y)]))
        self.plotOfFitDep.yData.append(_np.array([_np.min(y),_np.max(y)]))
        self.plotOfFitDep.yLegendLabel.append('ideal fit line')
        self.plotOfFitDep.marker.append('')
        self.plotOfFitDep.linestyle.append('-')
        self.plotOfFitDep.color.append('r')
        self.plotOfFitDep.alpha.append(1.)
        self.plotOfFitDep.legendLoc=  'upper left'
        self.plotOfFitDep.title=r'R$^2$ = %.5f' % self.rSquared
        
        # print results to screen
        print r'R2 =  %.5E' % self.rSquared
        print 'fit parameters'
        print('\n'.join('{}: {}'.format(*k) for k in enumerate(self.res.x)))
        
        # plot data
        if plot==True:
            if type(x) is _np.ndarray or len(x)==1:
                self.plotOfFit.plot()
            self.plotOfFitDep.plot()
            _plt.axes().set_aspect('equal') #, 'datalim'
        

def rSquared(y,f):
    """
    calculates R^2 of data fit
        
        
    Parameters
    ----------
    y : numpy.ndarray
        data being fit to, the dependent variable (NOT THE INDEPENDENT VARIABLE).  y is a functino of x, i.e. y=y(x)
    f : float
        fit data
        
    Returns
    -------
    : float 
        R^2 = 1 - \frac{\sum (f-y)^2 }{\sum (y-<y>)^2 }
    
    Reference
    ---------
    https://en.wikipedia.org/wiki/Coefficient_of_determination
    """
    yAve=_np.average(y);
    SSres = _np.sum( (y-f)**2 )
    SStot = _np.sum( (y-yAve)**2 )
    return 1-SSres/SStot
    
    
###############################################################################
### data management related

def listArrayToNumpyArray(inData):
    """
    Converts data from format a list of numpy.ndarrays to a 2D numpy.ndarray
    e.g. inData=[_np.array, _np.array, _np.array] to outData=_np.array([3,:])
    
    Parameters
    ----------
    inData : list (of numpy.ndarray)
        e.g. inData=[array([ 10.,  10.,  10.,  10.]),
                     array([ 15.,  15.,  15.,  15.]),
                     array([ 2.,  2.,  2.,  2.])]

    Returns
    -------
    outData : numpy.ndarray (2D)
        e.g. outData=   array([[ 10.,  15.,   2.],
                               [ 10.,  15.,   2.],
                               [ 10.,  15.,   2.],
                               [ 10.,  15.,   2.]])

    Notes
    -----
    Note that this code requires that all arrays in the list have the same
    length
    
    """
    outData = _np.array(inData)
    return outData
    