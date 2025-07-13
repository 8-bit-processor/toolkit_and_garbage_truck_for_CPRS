import socket
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# VistA RPC Broker delimiters
FS = b'\x1c'  # Field Separator (ASCII 28)
GS = b'\x1d'  # Group Separator (ASCII 29)
RS = b'\x1e'  # Record Separator (ASCII 30)
ET = b'\x04'  # End of Transmission (ASCII 4)

class VistARPCClient:
    """A client for making RPC calls to a VistA server."""

    def __init__(self, host, port, access_code, verify_code, context):
        """
        Initializes the VistARPCClient.

        Args:
            host (str): The VistA server hostname or IP address.
            port (int): The port number for the VistA RPC Broker.
            access_code (str): The user's access code for authentication.
            verify_code (str): The user's verify code for authentication.
            context (str): The application context for the RPC calls.
        """
        self.host = host
        self.port = port
        self.access_code = access_code
        self.verify_code = verify_code
        self.context = context
        self.socket = None
        self.connected = False

    def connect(self):
        """Establishes a connection to the VistA server."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            logging.info(f"Successfully connected to {self.host}:{self.port}")
            self._perform_handshake()
        except ConnectionRefusedError:
            logging.error(f"Connection refused. Is the VistA RPC Broker running on {self.host}:{self.port}?")
            self.connected = False
        except Exception as e:
            logging.error(f"An error occurred during connection: {e}")
            self.connected = False

    def _perform_handshake(self):
        """Performs the initial handshake with the VistA RPC Broker."""
        handshake_message = b'[XWB]10304\r\n'
        self.socket.sendall(handshake_message)
        response = self.socket.recv(4096)
        logging.info(f"Handshake response: {response.decode().strip()}")

    def login(self):
        """Logs in to the VistA server using the provided credentials."""
        if not self.connected:
            logging.error("Cannot log in without a connection.")
            return

        login_message = f"[XWB]10304\r\n{self.access_code};{self.verify_code}\r\n".encode()
        self.socket.sendall(login_message)
        response = self.socket.recv(4096)
        logging.info(f"Login response: {response.decode().strip()}")

        if not response.startswith(b'\x01'):
            logging.error("Login failed. Please check your access and verify codes.")
            self.disconnect()
            return False
        
        logging.info("Login successful.")
        return True

    def create_context(self):
        """Creates the application context for making RPC calls."""
        if not self.connected:
            logging.error("Cannot create context without a connection.")
            return

        self.call_rpc("XWB CREATE CONTEXT", [("literal", self.context)])

    def call_rpc(self, rpc_name, params=None):
        """
        Makes an RPC call to the VistA server.

        Args:
            rpc_name (str): The name of the RPC to call.
            params (list, optional): A list of tuples, where each tuple represents a parameter
                                     in the format (param_type, value). Defaults to None.

        Returns:
            str: The response from the RPC call, or None if an error occurs.
        """
        if not self.connected:
            logging.error("Cannot make an RPC call without a connection.")
            return None

        if params is None:
            params = []

        try:
            rpc_message_parts = [
                b'[XWB]10304',
                b'\r\n',
                rpc_name.encode(),
                b'\r\n'
            ]

            for param_type, value in params:
                rpc_message_parts.append(self._encode_rpc_param(param_type, value))

            rpc_message_parts.append(ET)
            final_rpc_message = b''.join(rpc_message_parts)

            self.socket.sendall(final_rpc_message)
            response = self.socket.recv(4096)
            decoded_response = response.decode().strip()
            logging.info(f"RPC response for '{rpc_name}': {decoded_response}")
            return decoded_response
        except Exception as e:
            logging.error(f"An error occurred during the RPC call: {e}")
            return None

    def _encode_rpc_param(self, param_type, value):
        """
        Encodes a single RPC parameter.

        Args:
            param_type (str): The type of the parameter (e.g., 'literal', 'reference', 'list').
            value: The value of the parameter.

        Returns:
            bytes: The encoded RPC parameter.
        """
        if param_type == 'literal':
            return b'L' + FS + str(value).encode() + GS
        elif param_type == 'reference':
            return b'R' + FS + str(value).encode() + GS
        elif param_type == 'list':
            encoded_list = b''
            for sub, val in value:
                encoded_list += str(sub).encode() + RS + str(val).encode() + RS
            return b'M' + FS + encoded_list + GS
        else:
            raise ValueError(f"Unknown parameter type: {param_type}")

    def disconnect(self):
        """Disconnects from the VistA server."""
        if self.socket:
            self.socket.close()
            self.socket = None
            self.connected = False
            logging.info("Disconnected from the server.")

if __name__ == "__main__":
    # --- Configuration ---
    VISTA_HOST = 'localhost'
    VISTA_PORT = 9297
    ACCESS_CODE = 'gtmuser'
    VERIFY_CODE = 'GT.M Rocks!'
    CONTEXT = 'XWB BROKER EXAMPLE'

    # --- Create and use the client ---
    client = VistARPCClient(VISTA_HOST, VISTA_PORT, ACCESS_CODE, VERIFY_CODE, CONTEXT)
    client.connect()

    if client.connected:
        if client.login():
            client.create_context()
            
            # --- Example RPC Call ---
            # Replace with the RPC you want to call
            rpc_to_call = "XWB LIST ALL RPCS"
            rpc_params = []  # No parameters for this RPC
            
            response = client.call_rpc(rpc_to_call, rpc_params)
            
            if response:
                print("\n--- RPC Result ---")
                print(response)
                print("--------------------")

        client.disconnect()
