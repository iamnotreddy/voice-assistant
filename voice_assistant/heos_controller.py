import socket

class HeosController:
    def __init__(self, ip, pid="1584681711"):
        self.ip = ip
        self.pid = pid
        self.port = 1255
    
    def send_command(self, command):
        try:
            # Create socket connection
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((self.ip, self.port))
            
            # Send command
            sock.sendall(f"{command}\r\n".encode('ascii'))
            
            # Read response
            response = b''
            while True:
                data = sock.recv(1024)
                if not data:
                    break
                response += data
                if b'\r\n' in response:
                    break
            
            # Close connection
            sock.close()
            
            # Return decoded response
            if response:
                return response.decode('ascii').strip()
            return None
            
        except Exception as e:
            print(f"Error connecting to speaker: {e}")
            return None
    
    def play_playlist(self):
        cmd = f"heos://browse/add_to_queue?pid={self.pid}&sid=9&cid=LIBPLAYLIST-892259848&mid=216313500&aid=1"
        return self.send_command(cmd)
    
    def pause(self):
        cmd = f"heos://player/set_play_state?pid={self.pid}&state=pause"
        return self.send_command(cmd)
    
    def play(self):
        cmd = f"heos://player/set_play_state?pid={self.pid}&state=play"
        return self.send_command(cmd)
    
    def volume_high(self):
        cmd = f"heos://player/set_volume?pid={self.pid}&level=35"
        return self.send_command(cmd)
    
    def volume_low(self):
        cmd = f"heos://player/set_volume?pid={self.pid}&level=20"
        return self.send_command(cmd)