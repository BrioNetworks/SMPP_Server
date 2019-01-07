
import sys,struct,time,string
import PCA_GenLib
import unbind



##############################################################################
###    Message Handler   	
##############################################################################
class Handler(unbind.Handler):	
	
 	def __init__(self):
		unbind.Handler.__init__(self)
	 	
	def getHandlerResponse(self):
		self.Message = None
    		return self.Message	
		
#########################################################################
# 
#
#########################################################################
class Parser(unbind.Parser):
	
	

	def __init__(self):
		try:
			Msg = "parser __init__"
			PCA_GenLib.WriteLog(Msg,9)
		
			unbind.Parser.__init__(self)
  			
  			Msg = "parser __init__ ok"
			PCA_GenLib.WriteLog(Msg,9)
		except:
 			Msg = "parser __init__  :<%s>,<%s>" % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)
			raise
