#!/usr/local/bin/python2.4
########################################################################################
#
# Filename:    PCA_SMPPServerSocket.py
#  
# Description
# =========== 
#
# This program is not to be copied or
# distributed without the express written consent of Author. No part of this
# program may be used for purposes other than those intended by Author.
#
# Author        : Michael Hsiao 
#
# Date   : 2010/10/20
# Desc   : Init - Submit_SM will route to Receiver if address match
# Date   :2017/10/26
# Desc   : upddte routint to routing by sms_text for Singtel project mo_copy/mt_copy 

########################################################################################

import sys, time,string,struct,re
import select
import socket
import PCA_GenLib
import PCA_Parser
import PCA_XMLParser
import PCA_DLL
import PCA_ServerSocket


###############################################################################
## 
###############################################################################
class Acceptor(PCA_ServerSocket.Acceptor):        

    ConnectionLoginState = {}   
    bind_recever_socket_fd = {}   
    def __init__(self,XMLCFG):
        try:
            Msg = "ResponseHandler Init ..."
            PCA_GenLib.WriteLog(Msg,9)

            PCA_ServerSocket.Acceptor.__init__(self,XMLCFG)			
            Tag = "Handler"
            dll_file_name = PCA_XMLParser.GetXMLTagValue(XMLCFG,Tag)
            Msg = "dll_file_name=<%s> " % dll_file_name
            PCA_GenLib.WriteLog(Msg,0)
            
            

            Script_File = PCA_DLL.DLL(dll_file_name)	

            factory_function="Parser"
            factory_component = Script_File.symbol(factory_function)
            self.parser = factory_component()
            factory_function="Handler"
            factory_component = Script_File.symbol(factory_function)
            self.handler  = factory_component()			
            self.parser.setContentHandler(self.handler )
            
            Tag = "Routing"
            self.msg_routing = PCA_XMLParser.GetXMLTagValue(XMLCFG,Tag)
            Msg = "msg_routing = <%s> " % self.msg_routing
            PCA_GenLib.WriteLog(Msg,0)
            
            Msg = "ResponseHandler Ok ..."
            PCA_GenLib.WriteLog(Msg,9)
        except:
            Msg = "ResponseHandler error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
            PCA_GenLib.WriteLog(Msg,0)
            raise
    ########################################################		
    ## Wating Client Connection by non-blocking I/O       ##
    ##						      ##
    ########################################################
    def dispatcher(self,TimeOut=2.0):
        try:
            Msg = "dispatcher server starting"
            PCA_GenLib.WriteLog(Msg,1)
            
            while 1:
                Msg = "listener dispatcher server loop"
                PCA_GenLib.WriteLog(Msg,9)

                readables, writeables, exceptions = select.select(self.ReadSet, [], [],TimeOut)    				
                for self.SocketConnection in readables:
                    ##################################
                    #### for ready input sockets #####
                    ##################################
                    if self.SocketConnection in self.SocketConnectionPool:  
                    ####################################
                    ## port socket: accept new client ##
                    ## accept should not block	  ##
                    ####################################
                        connection, address = self.SocketConnection.accept()
                        Msg = 'Dispatcher New Connection <%s> from :%s' % (id(connection),address)   # connection is a new socket 
                        PCA_GenLib.WriteLog(Msg,1)   
                        
                        self.ReadSet.append(connection)   # add to select list, wait
                        self.WriteSet.append(connection)  # add to select list, wait
                        
                        self.ConnectionLoginState[id(connection)] = 'N'
                        Msg = "Set ConnectionLoginState <%s> to N " % id(connection)
                        PCA_GenLib.WriteLog(Msg,1)
                        
                    else:
                        try:
                        
                            ClientMessage = self.SocketConnection.recv(1)
                            if not ClientMessage:
                                Msg = "Client Close Connection ..id=%s" % id(self.SocketConnection)
                                PCA_GenLib.WriteLog(Msg,1)
                                self.SocketConnection.close()                   # close here and remv from
                                self.ReadSet.remove(self.SocketConnection)      # del list else reselected 
                                self.WriteSet.remove(self.SocketConnection)     # del list else reselected 
                                Msg = "Del ConnectionLoginState <%s>" % id(self.SocketConnection)
                                PCA_GenLib.WriteLog(Msg,1)
                                del self.ConnectionLoginState[id(self.SocketConnection)]

                                for  address in self.bind_recever_socket_fd.keys():
                                
                                    if id(self.bind_recever_socket_fd[address]) == id(self.SocketConnection):
                                        try:
                                    
                                            Msg = "delete from self.bind_recever_socket_fd address=<%s>,socket_fd=<%s>" % (address,id(self.bind_recever_socket_fd[address]))
                                            PCA_GenLib.WriteLog(Msg,1)
                                            del self.bind_recever_socket_fd[address] 
                                        except:  
                                            Msg = "delete error ignore <%s>,<%s> " % (sys.exc_type,sys.exc_value)
                                            PCA_GenLib.WriteLog(Msg,0)	

                            else:
                                ###################################
                                ### Got Data Message From Client ##
                                ###################################
                                self.handle_event(self.SocketConnection,ClientMessage)
   
                        except socket.error:
                            Msg = "dispatcher socket error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
                            PCA_GenLib.WriteLog(Msg,0)	
                            
                            self.SocketConnection.close()                   # close here and remv from
                            self.ReadSet.remove(self.SocketConnection)      # del list else reselected 
                            self.WriteSet.remove(self.SocketConnection)     # del list else reselected 
                            del self.ConnectionLoginState[id(self.SocketConnection)]
                            try:
                              for  address in self.bind_recever_socket_fd.keys():
                                if id(self.bind_recever_socket_fd[address]) == id(self.SocketConnection):
                                    del self.bind_recever_socket_fd[address] 									
                                    Msg = "delete from self.bind_recever_socket_fd address=<%s>,socket_fd=<%s>" % (address,id(self.bind_recever_socket_fd[address]))
                                    PCA_GenLib.WriteLog(Msg,1)
                                    break
                            except:
                              Msg = "delete key error,ignore : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
                              PCA_GenLib.WriteLog(Msg,0)	
                                    
            Msg = "Normal end of dispatcher"
            PCA_GenLib.WriteLog(Msg,0)	
         
        except :
            Msg = "dispatcher error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
            PCA_GenLib.WriteLog(Msg,0)	
        
            Msg = "Error end of dispatcher"
            PCA_GenLib.WriteLog(Msg,0)
            time.sleep(2)		
            raise
   
   

    ########################################################		
    ## 						      ##
    ##						      ##
    ########################################################					
    def handle_event(self,SocketEventFD,ClientMessage):
        try:
            Msg = "handle_event Init"
            PCA_GenLib.WriteLog(Msg,9)
            
            
            #######################################################
            ##	 Read Request from Client 		    ###
            ##						    ###
            #######################################################
            
            Message = self.readDataFromSocket(SocketEventFD,Length=3,TimeOut = 10.0,ReadAttempts = 1)
            if Message == None:
                Msg = "read SMPP length error "
                PCA_GenLib.WriteLog(Msg,1)
                raise socket.error
            Msg = "DEBUG recv from Client =\n%s" % PCA_GenLib.HexDump(Message)
            PCA_GenLib.WriteLog(Msg,2)
            
            MessageLength = ClientMessage+Message
            MessageLength_Int = struct.unpack("!i",MessageLength)[0]
            
            if (MessageLength_Int != 0) and (MessageLength_Int < 4096):	
            
                Message = self.readDataFromSocket(SocketEventFD,Length=MessageLength_Int-4,TimeOut = 5.0,ReadAttempts = 1)
                if Message == None:
                    Msg = "read SMPP PDU error "
                    PCA_GenLib.WriteLog(Msg,1)
                    raise socket.error				
                
            else:
                Msg = "read SMPP PDU error incorrect length = <%s> " % MessageLength_Int
                PCA_GenLib.WriteLog(Msg,1)
                raise socket.error	

                
            SocketMessage = MessageLength + Message
            
            Msg = "recv from Client =\n%s" % PCA_GenLib.HexDump(SocketMessage)
            PCA_GenLib.WriteLog(Msg,2)
            self.parser.parse(SocketMessage)
            response_message = self.handler.getHandlerResponse()	
            ServerID = self.handler.getTID()
            DebugStr = self.handler.getDebugStr()
            if response_message != None:
                command_id = self.handler.getCOMMAND_ID()
                
                Msg = "command_id=<%s>" % command_id
                PCA_GenLib.WriteLog(Msg,2)  

                if command_id[-4:] == "resp":
                    Msg = "SMPP response message no need to ack command_id=<%s>" % command_id
                    PCA_GenLib.WriteLog(Msg,1)  
                else:
                
                    Msg = "send back to Client =\n%s" % PCA_GenLib.HexDump(response_message)
                    PCA_GenLib.WriteLog(Msg,2)
                    result = self.sendDataToSocket(SocketEventFD,response_message,TimeOut=2,WriteAttempts=3)
                    
                    if result != None:
                        Msg = "send back to client ok : data recv from client : ServerID=<%s>,%s" % (ServerID,DebugStr)
                        PCA_GenLib.WriteLog(Msg,1)  
                         
                        if command_id == "bind_receiver" or command_id == "bind_tranceiver" :
                            Msg = "save socket fd and address range"
                            PCA_GenLib.WriteLog(Msg,2)  
                            
                            if self.msg_routing == "Address":
                                address_range = self.handler.getADDRESS_RANGE()
                            
                                Msg = "save to bind_recever_socket_fd address_range=<%s>,SocketEventFD=<%s>" % (address_range,id(SocketEventFD))
                                PCA_GenLib.WriteLog(Msg,1)  
                                self.bind_recever_socket_fd[address_range] = SocketEventFD
                            else:
                                AIM = self.handler.getSystem_ID()
                            
                                Msg = "save to bind_recever_socket_fd AIM=<%s>,SocketEventFD=<%s>" % (AIM,id(SocketEventFD))
                                PCA_GenLib.WriteLog(Msg,1)  
                            
                                self.bind_recever_socket_fd[AIM] = SocketEventFD
                             
                        elif command_id == "submit_sm":
                            
                            Msg = "check destination address"
                            PCA_GenLib.WriteLog(Msg,2)  
                            
                             
                            if self.msg_routing == "Address":
                           
                                dest_address = self.handler.getDEST_ADDR()
                            else:
                                dest_address = self.handler.getTXT()
                            Msg = "dest_address = <%s>" % dest_address
                            PCA_GenLib.WriteLog(Msg,2)  
                             
                            Msg = "check if need to send delivery sm to exists bind_recever connection"
                            PCA_GenLib.WriteLog(Msg,2)

                            if string.find(DebugStr,"registered_delivery = <1>") == -1:
                              Msg = "submit sm did not request DR , ignore send deliver sm by setting dest_address=na"
                              PCA_GenLib.WriteLog(Msg,2)
                              dest_address = 'na'

                            found_receiver = 0
                            for  address in self.bind_recever_socket_fd.keys():
                            
                                Msg = "debug connected socket info <%s>" % address
                                PCA_GenLib.WriteLog(Msg,2)
                                #if re.compile(address).search(dest_address) != None:
                                if dest_address.find(address) != -1:
                                
                                    Msg = "found a receiver to delivery dest_addr = <%s>,receiver bind address=<%s>,socket_fd=<%s>" % (dest_address,address,id(self.bind_recever_socket_fd[address]))
                                    PCA_GenLib.WriteLog(Msg,1)
                                    found_receiver = 1
                                    break
                                     
                            if found_receiver == 1 and dest_address != 'na':
                            
                                Msg = "delivery sm to receiver socket_fd = <%s>" % id(self.bind_recever_socket_fd[address])
                                PCA_GenLib.WriteLog(Msg,1)
                                message_id = self.handler.getMessage_ID()
                                Msg = "delivery sm message id = <%s>" % (message_id)
                                PCA_GenLib.WriteLog(Msg,1)
                                delivery_sm = self.handler.getDELIVER_SM_PDU()

                                ############################################
                                # convert submit_sm to delivery_sm
                                # this use only for echo test 
                                ############################################
                                #delivery_sm = SocketMessage[0:7]+chr(0x05)+SocketMessage[8:]
                                
                                try:
                                    Msg = "send delivery sm to receiver =\n%s" % PCA_GenLib.HexDump(delivery_sm)
                                    PCA_GenLib.WriteLog(Msg,2)
                                    
                                    result = self.sendDataToSocket(self.bind_recever_socket_fd[address],delivery_sm,TimeOut=2,WriteAttempts=3)
                                    
                                    if result != None:
                                    
                                        Msg = "send delivery sm to receiver ok : socket_fd = <%s>" % id(self.bind_recever_socket_fd[address])
                                        PCA_GenLib.WriteLog(Msg,1)  

                                    else:
                                        Msg = "send delivery sm to receiver failure : socket_fd = <%s>" % id(self.bind_recever_socket_fd[address])
                                        PCA_GenLib.WriteLog(Msg,1)  
                                except socket.error:
                                    Msg = "send delivery sm to receiver socket failure ignore : socket_fd = <%s>" % id(self.bind_recever_socket_fd[address])
                                    PCA_GenLib.WriteLog(Msg,1)  
                            else:
                                    Msg = "did not find any receiver for this : %s" % dest_address
                                    PCA_GenLib.WriteLog(Msg,2)  
                                    
                    else:
                        Msg = "send back to client failure timeout : data recv from client : ServerID=<%s>,%s " % (ServerID,DebugStr)
                        PCA_GenLib.WriteLog(Msg,1)  
                    
                    
            else:
                Msg = "Error unknow response"
                PCA_GenLib.WriteLog(Msg,1)	
            
            
            Msg = "handle_event OK"
            PCA_GenLib.WriteLog(Msg,9)			
        except:
            Msg = "handle_event Error :<%s>,<%s>" % (sys.exc_type,sys.exc_value)
            PCA_GenLib.WriteLog(Msg,0)
            raise	    
