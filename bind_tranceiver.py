
import sys,struct,time,string
import PCA_GenLib
import unbind



##############################################################################
###    Message Handler   	
##############################################################################
class Handler(unbind.Handler):	
	
 	def __init__(self):
		unbind.Handler.__init__(self)
	 
	 
	 
	def startDocument(self):
		self.address_range = 'undef'
		self.system_id = 'undef'
		
	
	def startElement(self, name, attrs):
		try:
			Msg = "startElement init"
			PCA_GenLib.WriteLog(Msg,9)
			
			self.MessageName = name		
			
			if name == "system_id":
				self.system_id = attrs
 			if name == "address_range":
				self.address_range = attrs
			
			Msg = "startElement OK"
			PCA_GenLib.WriteLog(Msg,9)        	
		except:
 			Msg = "startElement Error :<%s>,<%s>" % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)
			raise
				
	def getHandlerResponse(self):		
		system_id = "test smsc" + chr(0x00)
		self.Message = system_id
    		return self.Message	
	
	
	def getADDRESS_RANGE(self):
		return self.address_range	
		
        
        
	def getSystem_ID(self):
	        Msg = "bind tranceiver system_id = %s" % self.system_id
                PCA_GenLib.WriteLog(Msg,0)
		return self.system_id	

		
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

	
	
	def parse(self, source):
		try:
			Msg = "parser init"
			PCA_GenLib.WriteLog(Msg,9)	
			self.SOURCD_ID = 'HeartBeat'
			self.DebugStr = ' '
			orig_data = source
			name = 'none'	
			self.StartParsing = 1			
			
			
			start_pos = string.find(source,chr(0x00))			
			system_id = source[0:start_pos]			
			self.DebugStr = "system_id = <%s>" % system_id	
			
			name = "system_id"
			attrs = system_id
			content = attrs
			self.set_handler(name,attrs,content)
				
			source = source[start_pos+1:]
			start_pos = string.find(source,chr(0x00))
			password = source[0:start_pos]			
			self.DebugStr = "%s , password = <%s>" % (self.DebugStr,password)	
			
			
			source = source[start_pos+1:]
			start_pos = string.find(source,chr(0x00))
			system_type = source[0:start_pos]			
			self.DebugStr = "%s , system_type = <%s>" % (self.DebugStr,system_type)	
			
			source = source[start_pos+1:]
			interface_version = struct.unpack("!b",source[0])[0]			
			self.DebugStr = "%s , interface_version = <%s>" % (self.DebugStr,interface_version)	
			
			source = source[1:]
			ton = struct.unpack("!b",source[0])[0]			
			self.DebugStr = "%s , ton = <%s>" % (self.DebugStr,ton)	
			
			source = source[1:]
			npi = struct.unpack("!b",source[0])[0]			
			self.DebugStr = "%s , npi = <%s>" % (self.DebugStr,npi)	
			
			source = source[1:]
			start_pos = string.find(source,chr(0x00))
			address_range = source[0:start_pos]	
			
			name = "address_range"
			attrs = address_range
			content = attrs
			self.set_handler(name,attrs,content)
				
			
			self.DebugStr = "%s , address_range = <%s>" % (self.DebugStr,address_range)	
				
			if self.StartParsing == 1:
        			self._cont_handler.endDocument(self.DebugStr,self.TID,self.SOURCD_ID)
        		
        		
			Msg = "parser OK"
			PCA_GenLib.WriteLog(Msg,9)
		except:
 			Msg = "parser  :<%s>,<%s>,name=<%s>" % (sys.exc_type,sys.exc_value,name)
			PCA_GenLib.WriteLog(Msg,0)
			
			Msg = "orig data =\n%s" % PCA_GenLib.HexDump(orig_data)
			PCA_GenLib.WriteLog(Msg,0)
			
			Msg = "rest data =\n%s" % PCA_GenLib.HexDump(source)
			PCA_GenLib.WriteLog(Msg,0)
			if self.StartParsing == 1:
        			self._cont_handler.endDocument(self.DebugStr,self.TID,self.SOURCD_ID)
        		return
	        		
	        		
	
