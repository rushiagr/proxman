

error_codes = {
    'address_incorrect':
        'Enter proxy address in correct format.',
    'port_incorrect':
        'Proxy port should be an integer between 0 and 65535.',
    'credentials_incorrect':
        'Only username or only password cannot be null.'
}

class Credentials:
    """
    Class to hold the proxy credentials. Local variables http, https, and ftp
    holds dictionaries whose keys are 'user', 'password', 'proxy', and 'port'.
    
    Typical dictionary format of self.data:
    {
        'noproxy': False,
        'sameproxy': True,      # Implies that same proxy credentials for http,
                                # ftp and https
        'http': {
            'proxy': '192.168.0.4',
            'port': '3128',
            'user': 'rushi',
            'password': 'rushi_pass'
        }
    }
    
    """
    
    def __init__(self, data):
        self.data = data
        if self.data['noproxy'] is False:
            if self.data['sameproxy'] is True:
                self.data['https'] = self.data['http']
                self.data['ftp'] = self.data['http']
        
            

    def validate(self):
        """ 
        Checks if the credentials are in proper format. 
        Returns (possibly empty) list of errors.
        """
        
        errors = []

        # If we're not using proxy, validation not required
        if self.data['noproxy'] is True:
            return errors
        
        proxies = ['http', 'https', 'ftp']
                
        # Error checking for: proxy address
        for proxy in proxies:
            # Break loop if the error we're trying to find is already found
            if error_codes['address_incorrect'] in errors:
                break
            
            split_address = self.data[proxy]['proxy'].split('.')
            if len(split_address) is not 4:
                errors.append(error_codes['address_incorrect'])
                break
            else:
                for part in split_address:
                    if not part.isdigit():
                        errors.append(error_codes['address_incorrect'])
                        break
                    if int(part) > 255 or int(part) < 0:
                        errors.append(error_codes['address_incorrect'])
                        break
        
        # Error checking for: proxy port
        for proxy in proxies:
            port = self.data[proxy]['port']
            if not port.isdigit() or int(port) > 65535 or int(port) < 0:
                errors.append(error_codes['port_incorrect'])
                break
            
        # Error checking for: proxy username and password
        for proxy in proxies:
            user = self.data[proxy]['user']
            password = self.data[proxy]['password']
            
            if (len(user) is 0 and len(password) is not 0) or \
                    (len(user) is not 0 and len(password) is 0):
                errors.append(error_codes['credentials_incorrect'])
                break
            
        return errors
