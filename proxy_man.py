import os
import sys



UNSET_EXISTING_VARIABLES = 3
DO_NOTHING = 4




class ApplyProxy:
    def __init__(self, cred):
        if cred.data['noproxy'] is True:
            self.clearproxy(UNSET_EXISTING_VARIABLES)
        else:
                self.clearproxy(DO_NOTHING)
                self.update_files(cred)
        self.status = 'success'
            
    def clearproxy(self, state):
        """ Removes existing proxy from the system.
            if the value of state is UNSET_EXISTING_VARIABLES, it unsets the 
            existing proxy environment variables from the shells spawned after 
            this program is executed """

        # Clearing /etc/bash.bashrc file
        bashrc_file = open('/etc/bash.bashrc','r')
        bashrc_contents = bashrc_file.readlines()
        bashrc_file.close()

        bashrc_file = open('/etc/bash.bashrc', 'w')
        for i in range(len(bashrc_contents)):
            if bashrc_contents[i].lower().startswith(
                        'export http_proxy') or \
                    bashrc_contents[i].lower().startswith(
                        'export https_proxy') or \
                    bashrc_contents[i].lower().startswith(
                        'export ftp_proxy') or \
                    bashrc_contents[i].lower().startswith(
                        'unset http_proxy') or \
                    bashrc_contents[i].lower().startswith(
                        'unset ftp_proxy') or \
                    bashrc_contents[i].lower().startswith(
                        'unset https_proxy'):
                    
                bashrc_contents[i] = ''
        bashrc_file.write(''.join(bashrc_contents))
        
        if state == UNSET_EXISTING_VARIABLES:
            bashrc_file.write('unset http_proxy\n')
            bashrc_file.write('unset https_proxy\n')
            bashrc_file.write('unset ftp_proxy\n')
        
        bashrc_file.close()
        
        # Clearing /etc/environment file
        env_file = open('/etc/environment','r')
        env_contents = env_file.readlines()
        env_file.close()
        env_file = open('/etc/environment','w')
        for i in range(len(env_contents)):
            if env_contents[i].lower().startswith('http_proxy') or \
                    env_contents[i].lower().startswith('https_proxy') or \
                    env_contents[i].lower().startswith('ftp_proxy'):
                env_contents[i] = ''
        env_file.write(''.join(env_contents))
        env_file.close()
        
        # Clearing /etc/apt/apt.conf file
        aptconf_file = open('/etc/apt/apt.conf', 'w')
        aptconf_file.write('')
        aptconf_file.close()
        
        ## clear proxy from synaptic
        if os.path.exists('/root/.synaptic/synaptic.conf'):
            sconf_file = open('/root/.synaptic/synaptic.conf', 'r')
            sconf_contents = sconf_file.readlines()
            sconf_file.close()
            
            for i in range(len(sconf_contents)):
                if sconf_contents[i].find('useProxy') > -1:
                    sconf_contents[i] = list(sconf_contents[i])
                    sconf_contents[i][12] = '0'
                    sconf_contents[i] = ''.join(sconf_contents[i])
                    break
            
            sconf_file = open('/root/.synaptic/synaptic.conf', 'w')
            sconf_file.writelines(sconf_contents)
            sconf_file.close()

        
    def update_files(self, cred):
        """
        Updates all the four files with provided proxy values.
        Assumes all four files is already clear of all previous proxies.
        """

        combo_string = {}
        for proxy in ['http', 'https', 'ftp']:
            combo_string[proxy] = cred.data[proxy]['proxy'] +':'+ \
                                    cred.data[proxy]['port']
            if cred.data[proxy]['use_auth'] is True:
                combo_string[proxy] = cred.data[proxy]['user'] +':'+ \
                                    cred.data[proxy]['password'] +'@'+ \
                                    combo_string[proxy]
        
        # Update /etc/bash.bashrc, /etc/environment, and /etc/apt/apt.conf file
        bashrc_file = open('/etc/bash.bashrc', 'a')
        env_file = open('/etc/environment', 'a')
        aptconf_file = open('/etc/apt/apt.conf', 'a')

        protocols = ['http', 'https', 'ftp']
        
        for i in protocols:
            bashrc_file.write('export ' + i + '_proxy=' + i + '://' + combo_string[i] + '/\n')
            env_file.write(i + '_proxy="' + i + '://' + combo_string[i] + '/"\n')
            aptconf_file.write('Acquire::' + i + '::Proxy "' + i + '://' + combo_string[i] + '/";\n')
            
        bashrc_file.close()
        env_file.close()
        aptconf_file.close()
        
        # Update /root/.synaptic/synaptic.conf file
        if os.path.exists('/root/.synaptic/synaptic.conf'):
            sconf_file = open('/root/.synaptic/synaptic.conf', 'r')
            sconf_contents = sconf_file.readlines()
            sconf_file.close()
            
            value = {
                'useProxy'      : '1',
                'httpProxyUser' : cred.data['http']['user'],
                'httpProxyPass' : cred.data['http']['password'],
                'httpProxy'     : cred.data['http']['proxy'],
                'httpProxyPort' : cred.data['http']['port'],
                'ftpProxy'      : cred.data['ftp']['proxy'],
                'ftpProxyPort'  : cred.data['ftp']['port'],
                }
            
            def change_value(string):
                """
                For a line 'string' of synaptic.conf file, it assigns to 'name' attribute a value 'value'
                """
                
                split_string = string.split('"')
                if len(split_string) == 3:
                    string_name = split_string[0].split()[0]
                    string_value = split_string[1]
                    
                    if value.has_key(string_name) == True:
                        string_value = value[string_name]
                        updated_string = '  ' + string_name + ' "' + string_value + '";\n'
                        return updated_string
                return string
                
            for i in range(len(sconf_contents)):
                sconf_contents[i] = change_value(sconf_contents[i])
            
            sconf_file = open('/root/.synaptic/synaptic.conf', 'w')
            sconf_file.writelines(sconf_contents)
            sconf_file.close()
