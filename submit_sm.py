
import sys,struct,time,string
import PCA_GenLib
import PCA_Parser
import random
import PCA_SMPPMessage

##############################################################################
###    Message Handler   	
##############################################################################
class Handler(PCA_Parser.ContentHandler):	
	
 	def __init__(self):
		PCA_Parser.ContentHandler.__init__(self)
	 	self.TXT = 'undef_ext'
	 	self.message_id = 'undef_id'
                self.DELIVER_SM_PDU = 'undef_submit'
	      
	def startElement(self, name, attrs):
		self.TID = ''
		self.SOURCD_ID = "HeartBeat"
		
		if name == "dest_address":
	       	  self.dest_address = attrs
		if name == "TXT":
		  self.TXT = attrs
		if name == "message_id":
		  self.message_id = attrs
		if name == "DELIVER_SM_PDU":
		  self.DELIVER_SM_PDU = attrs
	          #Msg = "DELIVER_SM_PDU we got in submit_sm"
		  #PCA_GenLib.WriteLog(Msg,9)
						
	def endDocument(self,debugstr,TID,SOURCD_ID ):
        	self.DebugStr = debugstr
        	self.TID = TID
        	self.SOURCD_ID = SOURCD_ID
	
	def getSOURCD_ID(self):	
		return self.SOURCD_ID	

	def getHandlerResponse(self):
		
		self.Message = self.message_id + chr(0x00)
    		return self.Message	
	
	def getDEST_ADDR(self):	
		return self.dest_address	
	
	def getTXT(self):	
		return self.TXT	
	def getDELIVER_SM_PDU(self):	
		return self.DELIVER_SM_PDU

#########################################################################
# 
#
#########################################################################
class Parser(PCA_Parser.Parser):
	
	
	DebugStr = 'na'
	SMS_TYPE='na'
	
	TID = 'na'
	
	Service_Type = 'na'
	SOURCD_ID = 'HeartBeat'
        deliver_sm = chr(0x00)+chr(0x0)+chr(0x00)+chr(0x05)
	
	#Debug_Str_Dict = {}
	

	def __init__(self):
		try:
			Msg = "parser __init__"
			PCA_GenLib.WriteLog(Msg,9)
		
			PCA_Parser.Parser.__init__(self)
		        seq_no = random.randint(1,100000)
                        self.SMPPWriter = PCA_SMPPMessage.SMPP_PDU_Writer(seq_no)
  			
  			Msg = "parser __init__ ok"
			PCA_GenLib.WriteLog(Msg,9)
		except:
 			Msg = "parser __init__  :<%s>,<%s>" % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)
			raise
	
	def set_handler(self,name,attrs,content):
			
		self._cont_handler.startElement(name, attrs)        		
		self._cont_handler.characters(content)
        	self._cont_handler.endElement(name)
        	
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
			service_type = source[0:start_pos]			
			self.DebugStr = "system_id = <%s>" % service_type	
			
			source = source[start_pos+1:]
                        submit_sm_source_addr_ton = source[0]
			source_addr_ton = struct.unpack("!b",source[0])[0]			
			self.DebugStr = "%s , source_addr_ton = <%s>" % (self.DebugStr,source_addr_ton)	
			
			source = source[1:]
                        submit_sm_source_addr_npi = source[0]
			source_addr_npi = struct.unpack("!b",source[0])[0]			
			self.DebugStr = "%s , source_addr_npi = <%s>" % (self.DebugStr,source_addr_npi)	
			
			source = source[1:]
			start_pos = string.find(source,chr(0x00))
			source_addr = source[0:start_pos]
                        submit_sm_source_addr = source_addr
			self.DebugStr = "%s , source_addr = <%s>" % (self.DebugStr,source_addr)	
			
			source = source[start_pos+1:]
                        submit_sm_dest_addr_ton = source[0]
			dest_addr_ton = struct.unpack("!b",source[0])[0]
			self.DebugStr = "%s , dest_addr_ton = <%s>" % (self.DebugStr,dest_addr_ton)	
			
			source = source[1:]
                        submit_sm_dest_addr_npi = source[0]
			dest_addr_npi = struct.unpack("!b",source[0])[0]			
			self.DebugStr = "%s , dest_addr_npi = <%s>" % (self.DebugStr,dest_addr_npi)	
			
			source = source[1:]
			start_pos = string.find(source,chr(0x00))
			dest_addr = source[0:start_pos]
                        submit_sm_dest_addr = dest_addr
			self.DebugStr = "%s , dest_addr = <%s>" % (self.DebugStr,dest_addr)

			name = "dest_address"
			attrs = dest_addr
			content = attrs
			self.set_handler(name,attrs,content)
			
						
			source = source[start_pos+1:]
			esm_class = struct.unpack("!b",source[0])[0]
			self.DebugStr = "%s , esm_class = <%s>" % (self.DebugStr,esm_class)
			
			source = source[1:]
			protocol_id = struct.unpack("!b",source[0])[0]
			self.DebugStr = "%s , protocol_id = <%s>" % (self.DebugStr,protocol_id)
				
			source = source[1:]
			priority_flag = struct.unpack("!b",source[0])[0]
			self.DebugStr = "%s , priority_flag = <%s>" % (self.DebugStr,priority_flag)
			
			source = source[1:]
			start_pos = string.find(source,chr(0x00))
			schedule_delivery_time = source[0:start_pos]
			self.DebugStr = "%s , schedule_delivery_time = <%s>" % (self.DebugStr,schedule_delivery_time)
			
			source = source[start_pos+1:]
			start_pos = string.find(source,chr(0x00))
			validity_period = source[0:start_pos]
			self.DebugStr = "%s , validity_period = <%s>" % (self.DebugStr,validity_period)
				
  		        CurrentSeconds = time.time() + random.randint(1,100000)
		        date_tuple =  time.localtime(CurrentSeconds)		
		        message_id = "%02d%02d%02d%02d" % (date_tuple[2:6])
		        Msg = "submit sm response msg_id=<%s>" % message_id
		        PCA_GenLib.WriteLog(Msg,2)	
			name = "message_id"
			attrs = message_id
			content = attrs
			self.set_handler(name,attrs,content)

			source = source[start_pos+1:]
			registered_delivery = struct.unpack("!b",source[0])[0]
			self.DebugStr = "%s , registered_delivery = <%s>" % (self.DebugStr,registered_delivery)

			source = source[1:]
			replace_if_present_flag = struct.unpack("!b",source[0])[0]
			self.DebugStr = "%s , replace_if_present_flag = <%s>" % (self.DebugStr,replace_if_present_flag)
			
			source = source[1:]
			data_coding = struct.unpack("!b",source[0])[0]
			self.DebugStr = "%s , data_coding = <%s>" % (self.DebugStr,data_coding)
			
			source = source[1:]
			sm_default_msg_id = struct.unpack("!b",source[0])[0]
			self.DebugStr = "%s , sm_default_msg_id = <%s>" % (self.DebugStr,sm_default_msg_id)
			
			source = source[1:]
			sm_length = struct.unpack("!B",source[0])[0]
			self.DebugStr = "%s , sm_length = <%s>" % (self.DebugStr,sm_length)
			
			source = source[1:]
			short_message = source[:sm_length]
			self.DebugStr = "%s , short_message = <%s>" % (self.DebugStr,short_message)
            
			name = "TXT"
			attrs = short_message
			content = attrs
			self.set_handler(name,attrs,content)

                        # submit sm request for DR , prepare delivery sm pdu
                        if registered_delivery == 1:
                          service_type = chr(0x00)
                          source_addr_ton = submit_sm_dest_addr_ton
                          source_addr_npi = submit_sm_dest_addr_npi
                          source_addr = submit_sm_dest_addr+chr(0x00)
                          dest_addr_ton = submit_sm_source_addr_ton
                          dest_addr_npi = submit_sm_source_addr_npi
                          dest_address = submit_sm_source_addr+chr(0x00)
                          esm_class = chr(0x00)
                          protocol_id = chr(0x00)
                          priority_flag = chr(0x00)
                          schedule_delivery_time = chr(0x00)
                          validity_period = chr(0x00)
                          registered_delivery = chr(0x00)
                          replace_if_present_flag = chr(0x00)
                          data_coding = chr(0x00)
                          sm_default_msg_id = chr(0x00)
  		          CurrentSeconds = time.time()
		          date_tuple =  time.localtime(CurrentSeconds)		
                          name = "SUBMIT_DATE"
	                  submit_date = "%04d%02d%02d%02d%02d" % (date_tuple[0:5])
	                  submit_date = submit_date[2:]

                          deliver_date = submit_date
                          name = "TEXT"
                          text = "id:%s sub:001 dlvrd:001 submit date:%s done date:%s stat:DELIVRD err:000 text:%s"  % (message_id,submit_date,deliver_date,content[0:20])

                          short_message = text
			  Msg = "delivery_sm_text=<%s>" % text
			  PCA_GenLib.WriteLog(Msg,1)
                          sm_length =  chr(len(short_message))
                          self.SMPPWriter.ConstructHeader(self.deliver_sm)
                          parm1 = service_type + source_addr_ton + source_addr_npi + source_addr
                          parm2 = dest_addr_ton + dest_addr_npi + dest_address + esm_class + protocol_id + priority_flag
                          parm3 = schedule_delivery_time + validity_period + registered_delivery
                          #msg:set_param_hex('smpp.tlv_0423', '030000') -- error_code: type GSM no error
                          reference_message_id = chr(0x00)+chr(0x1e)+chr(0x00)+chr(0x09)+ message_id+chr(0x00)
                          message_state = chr(0x04)+chr(0x27)+chr(0x00)+chr(0x01)+chr(0x02)
                          parm4 =  replace_if_present_flag+ data_coding +sm_default_msg_id+sm_length + short_message + reference_message_id + message_state

                          DELIVER_SM_PDU = self.SMPPWriter.ConstructParameter(parm1,parm2,parm3,parm4)
			  #Msg = "PCA Construct DELIVERY SM PDU"
			  #PCA_GenLib.WriteLog(Msg,1)

			  #Msg = " data =\n%s" % PCA_GenLib.HexDump(DELIVER_SM_PDU)
			  #PCA_GenLib.WriteLog(Msg,0)
			  name = "DELIVER_SM_PDU"
			  attrs = DELIVER_SM_PDU
			  content = attrs
			  self.set_handler(name,attrs,content)
			

				
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
	        		
	        		
	
