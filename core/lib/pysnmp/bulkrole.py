"""
   SNMP transport class.

   Sends & receives SNMP messages to multiple destinations in bulk.

   Written by Ilya Etingof <ilya@glas.net>, 1999-2002.

"""
import socket

# Import PySNMP components
from . import role
from . import v1, v2c

class Error(role.Error):
    """Base class for bulkrole module
    """
    pass

class BadArgument(Error):
    """Bad argument given
    """
    pass

class manager:
    """Send SNMP messages to multiple destinations and receive
       replies.
    """
    def __init__(self, iface=('0.0.0.0', 0)):
        # Initialize defaults
        self.iface = iface
        self.clear()

        # Set defaults to public attributes
        self.retries = 3
        self.timeout = 1

    #
    # Implement list interface
    #

    def __str__(self):
        """
        """
        return str(self._requests)

    def __repr__(self):
        """
        """
        return repr(self._requests)

    def clear(self):
        """Clear the list of sessions and prepare for next round
           of append->dispatch->subscript cycle.
        """
        self._requests = []
        self._responses = []
        self._durty = 0
        
        # [Re-]create SNMP manager transport
        self.transport = role.manager(self.iface)

    def append(self, xxx_todo_changeme):
        """
           append((dst, req))

           Create transport session destined to "agent" (a tuple of (host, port)
           where host is a string and port is an integer) and queue SNMP
           "request" message (string) to be sent to "agent".

           All queued request messages will be sent upon self.dispatch() method
           invocation.
        """
        (dst, req) = xxx_todo_changeme
        if self._durty:
            raise ValueError('List is not valid for update (try clear())')

        if req['request_id'] in [dst_req1[1]['request_id'] for dst_req1 in self._requests]:
            raise BadArgument('Duplicate request IDs in queue')

        self._requests.append((dst, req))

    def __setitem__(self, idx, xxx_todo_changeme5):
        """
        """
        (dst, req) = xxx_todo_changeme5
        if self._durty:
            raise ValueError('List is not valid for update (try clear())')

        if req['request_id'] in [dst_req2[1]['request_id'] for dst_req2 in self._requests]:
            raise BadArgument('Duplicate request IDs in queue')
        
        try:
            self._requests[idx] = (dst, req)

        except IndexError:
            raise IndexError('Request index out of range')

    def __getitem__(self, idx):
        """
        """
        try:
            return self._requests[idx]

        except IndexError:
            raise IndexError('Request index out of range')

    def __len__(self):
        """
        """
        return len(self._requests)
                   
    def count(self, val):
        """XXX
        """
        return self._requests.count(val)

    def index(self, xxx_todo_changeme6):
        """
        """
        (dst, req) = xxx_todo_changeme6
        if self._durty:
            raise ValueError('List is not valid for update (try clear())')

        try:
            return self._requests.index((dst, req))

        except ValueError:
            raise ValueError('No such request in queue')

    def insert(self, idx, xxx_todo_changeme7):
        """
        """
        (dst, req) = xxx_todo_changeme7
        if self._durty:
            raise ValueError('List is not valid for update (try clear())')

        if req['request_id'] in [dst_req3[1]['request_id'] for dst_req3 in self._requests]:
            raise BadArgument('Duplicate request IDs in queue')
        
        try:
            return self._requests.insert(idx, (dst, req))

        except IndexError:
            raise IndexError('Request index out of range')

    def remove(self, xxx_todo_changeme8):
        """
        """
        (dst, req) = xxx_todo_changeme8
        try:
            return self._requests.remove((dst, req))

        except ValueError:
            raise ValueError('No such request in queue')

    def pop(self, idx=-1):
        """
        """
        try:
            return self._requests.pop(idx)

        except IndexError:
            raise IndexError('Request index out of range')

    #
    # The main I/O method
    #
    def dispatch(self):
        """
           dispatch()
           
           Send pending SNMP requests and receive replies (or timeout).
        """
        # Indicate that internal queue might change
        self._durty = 1

        # Resolve destination hostnames to IP numbers for later comparation
        try:
            self._requests = [((socket.gethostbyname(dst_req[0][0]), \
                                   dst_req[0][1]), dst_req[1]) for dst_req in self._requests]

        except socket.error as why:
            raise BadArgument(why)

        # Initialize a list of responses
        self._responses = [(dst_req4[0], None) for dst_req4 in self._requests]

        # Initialize retry counter
        retries = self.retries
        
        while retries:
            # Send out requests and prepare for waiting for replies
            for idx in range(len(self._requests)):
                # Skip completed session
                (src, rsp) = self._responses[idx]
                if rsp is not None:
                    continue

                (dst, req) = self._requests[idx]

                try:
                    self.transport.send(req.encode(), dst)
                    
                except role.Error:
                    # Ignore transport errors
                    pass

            # Collect responses from agents
            for (src, rsp) in self._responses:
                # Skip responded entities
                if rsp is not None:
                    continue

                # XXX Probably select() based multiplexing would better
                # serve timeouts...
                
                # Wait for response
                (response, src) = self.transport.receive()

                # Stop on timeout
                if response is None:
                    retries = retries - 1
                    break

                # Decode response
                (rsp, rest) = v2c.decode(response)

                # Try to match response message against pending
                # request messages
                for idx in range(len(self._requests)):
                    if (src, rsp) == self._requests[idx]:
                        self._responses[idx] = (src, rsp)
                        break
            else:
                # Everyone responded
                break
                
        # Replace list of requests with list of replies
        self._requests = self._responses            

