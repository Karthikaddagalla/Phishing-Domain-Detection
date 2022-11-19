import pandas as pd
import re
import whois
from datetime import datetime
import requests
import dns.resolver
import tldextract
import yarl
import sklearn
import urllib

print(sklearn.__version__)


class Url_DataFrame:
    """This class is mainly used to extract all the required features for our Machine Learning model from the given URL"""
    
    
    def __init__(self, url):
        self.link = url
        self.domain = self.domain_name_detect()
        
        self.df = pd.DataFrame(data = [0], columns = ["delete"])
        self.df.drop("delete", axis = 1, inplace = True)
        
        self.url_dataframe_preparation()

    
        
        
        
        
    def is_registered(self):
        """This method is used to check whether given url is registered or not and also assign no of days since it got activated
           and no of days it had to get expired."""
     
        try:
            whois_info = whois.whois(self.link)
            
            is_registered = bool(whois_info.domain_name)
        
        except Exception as e:
            is_registered = False
            print(e)
        
        finally:
            now_date = datetime.now()     #Present time but with no seconds given
            dt_string = now_date.strftime("%d/%m/%Y %H:%M:%S")      # Converting present time to string since we also need seconds
            dt_date = datetime.strptime(dt_string, '%d/%m/%Y %H:%M:%S')   # Converting string back to date time
        
        
            if is_registered:
                
                if type(whois_info.creation_date) == list:
                    creation_date = whois_info.creation_date[0]
                    
                else:
                    creation_date = whois_info.creation_date
                
                time_domain_activation = (dt_date) - (creation_date)
                
                if type(whois_info.expiration_date) == list:
                    expiry_date = whois_info.expiration_date[0]
                    
                else:
                    expiry_date = whois_info.expiration_date
                
                time_domain_expiration = (expiry_date) - (dt_date)
                self.df['time_domain_activation'] = time_domain_activation.days
                self.df['time_domain_expiration'] = time_domain_expiration.days
                    
            else:
                self.df['time_domain_activation'] = -1
                self.df['time_domain_expiration'] = -1
                
        
          
    def time_response(self):
        """This method is used to calculate the time response and if url contains email in it"""  
        
        # Checking for email in the url
        
        reg = re.findall(r"[A-Za-z0-9._%+-]+"
                         r"@[A-Za-z0-9.-]+"
                         r"\.[A-Za-z]{2,4}", self.link)

        if(len(reg)>0):
            self.df["email_in_url"] = 1
            
        else:
            self.df["email_in_url"] = 0
        
        # Finding time response of the website
        
        try:
            self.df['time_response'] = requests.get(self.link).elapsed.total_seconds()
            
        except Exception:
            self.df["time_response"] = float(0)
           
       
    
    def domain_name_detect(self):
        """This method is used for extracting the domain_name from the url"""
        
        if re.search("://", self.link):                    # Checking for protocol in the url
            main_url = self.link.split("/")[2]  
        
        else:
            main_url = self.link.split("/")[0]
    
    
        if re.search("^www", main_url):       # Removing the 3rd level domain it it exists
            domain_name = ".".join(main_url.split(".")[1:])
        
        else:
            domain_name = main_url
        
        return domain_name
    
    
    def check_http(self):
        if re.search("^http", self.link):
            return 4       # It contains http

        else:
            return 5       # It doesn't have an http

    
    def number_ns_mx_records(self):
        """This method gives the no of mx and ns records of our domain"""

        try:
            self.df["qty_nameservers"] = len(dns.resolver.resolve(self.domain, "NS"))
            
        except:
            self.df["qty_nameservers"] = 0
            
            
            
        try:
            self.df["qty_mx_servers"] = len(dns.resolver.resolve(self.domain, "mx"))
            
        except:
            self.df["qty_mx_servers"] = 0
            
    
    
    def resolved_ips(self):
        """This method is used for finding no resolved ips of the domain"""
        
        try:
           
        
            result = dns.resolver.resolve(self.domain, 'A')

#
            self.df["qty_ip_resolved"] = -1 if len(result) == 0 else len(result)
    
    
        except Exception:
            self.df["qty_ip_resolved"] = -1
    
            
            
          
    def tls_ssl_certificate(self):
        """This method is used to check if there is ssl certificate"""
        
        try: 
            
            if re.search("https", self.link):
                self.df["tls_ssl_certificate"] = 1
                
            else:
                self.df["tls_ssl_certificate"] = 0
                
            
        except Exception:
            self.df["tls_ssl_certificate"] = 0
            
    
    def server_client(self):
        val = bool(re.search(r'(server)|(client)',self.link))
        if(val):
            return 1
        else:
            return 0
            
    
    
    def check_link(self):
        """
            This method is to check whether the link is working or not!
        """
        
        try:
            request = requests.get(self.link)
            return 1
        except:
            return 0
    
        
       
    def vowels(self):
        """This method returns us the no of vowels in our domain name"""
        
        vowels = re.findall(r'[aeiou]+',self.domain)
        sum = 0
        for item in vowels:
            sum += len(item)
        return sum
    
    
    
    def domain_contains_ip(self):
        """This method is used to find if url contains ip address than the domain name"""
        
        
        if len(re.findall("[123456789]+", self.domain)) == 4 or len(re.findall("[123456789]+", self.domain)) == 6:
            return 1
        
        else:
            return 0
        
        
    def check_email_url(self):
        """
            A function to check whether email ID exist in the URL
        """
        reg = re.findall(r"[A-Za-z0-9._%+-]+"
                         r"@[A-Za-z0-9.-]+"
                         r"\.[A-Za-z]{2,4}", self.link)
        if(len(reg)>0):
            return 1
        else:
            return 0
        
        

     
    
    
    def url_dataframe_preparation(self):
        """This method is used to create the entire dataset from the given url"""
        
        
        try:
            
            # Entire URL
            
            url = yarl.URL(self.link)

            self.df['qty_dot_url'] = len(re.findall('[.]', self.link))
            self.df['qty_hyphen_url'] = len(re.findall('[-]', self.link))
            self.df['qty_underline_url'] = len(re.findall('[_]', self.link))
            self.df['qty_slash_url'] = len(re.findall('[/]', self.link))
            self.df['qty_questionmark_url'] = len(re.findall('[?]', self.link))
            self.df['qty_equal_url'] = len(re.findall('[=]', self.link))
            self.df['qty_at_url'] = len(re.findall('[@]', self.link))
            self.df['qty_and_url'] = len(re.findall('[&]', self.link))
            self.df['qty_exclamation_url'] = len(re.findall('[!]', self.link))
            self.df['qty_exclamation_url'] = len(re.findall('[!]', self.link))
            self.df['qty_space_url'] = len(re.findall('[ ]', self.link))
            self.df['qty_tilde_url'] = len(re.findall('[~]', self.link))
            self.df['qty_comma_url'] = len(re.findall('[,]', self.link))
            self.df['qty_plus_url'] = len(re.findall('[+]', self.link))
            self.df['qty_asterisk_url'] = len(re.findall('[*]', self.link))
            self.df['qty_hashtag_url'] = len(re.findall('[#]', self.link))
            self.df['qty_dollar_url'] = len(re.findall('[$]', self.link))
            self.df['qty_percent_url'] = len(re.findall('[%]', self.link))
            self.df['qty_tld_url'] = len(tldextract.extract(self.link).suffix)
            self.df['length_url'] = len(self.link)
            self.df['email_in_url'] = self.check_email_url()
            
            
            # Domain
            
            

            self.df['qty_dot_domain'] = len(re.findall('[.]', self.domain))
            self.df['qty_hyphen_domain'] = len(re.findall('[-]', self.domain))
            self.df['qty_underline_domain'] = len(re.findall('[_]', self.domain))
            self.df['qty_vowels_domain'] = self.vowels()
            self.df['domain_length'] = len(self.domain)
            self.df["domain_in_ip"] = self.domain_contains_ip()
            self.df['server_client_domain'] = self.server_client()
            
            
            
            # Directory            
            
            
            dirr = url.raw_path              # These gives the entire path after domain name
            lenn = len(dirr.split('/')) - 1  # Minus 1 to avoid the file name in the directory
            split_dir = dirr.split('/')
            directory = ''
            if (lenn > 1):
                for i in range(0, lenn):
                    directory += split_dir[i] + '/'
            
            print(split_dir)

            self.df['qty_dot_directory'] = len(re.findall('[.]', directory)) if len(directory) != 0 else -1
            self.df['qty_hyphen_directory'] = len(re.findall('[-]', directory)) if len(directory) != 0 else -1
            self.df['qty_underline_directory'] = len(re.findall('[_]', directory)) if len(directory) != 0 else -1
            self.df['qty_slash_directory'] = len(re.findall('[/]', directory)) if len(directory) != 0 else -1
            self.df['qty_questionmark_directory'] = len(re.findall('[?]', directory)) if len(directory) != 0 else -1
            self.df['qty_equal_directory'] = len(re.findall('[=]', directory)) if len(directory) != 0 else -1
            self.df['qty_at_directory'] = len(re.findall('[@]', directory)) if len(directory) != 0 else -1
            self.df['qty_and_directory'] = len(re.findall('[&]', directory)) if len(directory) != 0 else -1
            self.df['qty_exclamation_directory'] = len(re.findall('[!]', directory)) if len(directory) != 0 else -1
            self.df['qty_space_directory'] = len(re.findall('[ ]', directory)) if len(directory) != 0 else -1
            self.df['qty_tilde_directory'] = len(re.findall('[~]', directory)) if len(directory) != 0 else -1
            self.df['qty_comma_directory'] = len(re.findall('[,]', directory)) if len(directory) != 0 else -1
            self.df['qty_plus_directory'] = len(re.findall('[+]', directory)) if len(directory) != 0 else -1
            self.df['qty_asterisk_directory'] = len(re.findall('[*]', directory)) if len(directory) != 0 else -1
            self.df['qty_hashtag_directory'] = len(re.findall('[#]', directory)) if len(directory) != 0 else -1
            self.df['qty_dollar_directory'] = len(re.findall('[$]', directory)) if len(directory) != 0 else -1
            self.df['qty_percent_directory'] = len(re.findall('[%]', directory)) if len(directory) != 0 else -1
            self.df['directory_length'] = len(directory) if len(directory) != 0 else -1
            
            
            
            # File
            
            
            file = split_dir[-1]       # Since it is the last element in the directory list
            
            
            
            self.df['qty_dot_file'] = len(re.findall('[.]', file)) if len(file) != 0 else -1
            self.df['qty_hyphen_file'] = len(re.findall('[-]', file)) if len(file) != 0 else -1
            self.df['qty_underline_file'] = len(re.findall('[_]', file)) if len(file) != 0 else -1
            self.df['qty_slash_file'] = len(re.findall('[/]', file)) if len(file) != 0 else -1
            self.df['qty_questionmark_file'] = len(re.findall('[?]', file)) if len(file) != 0 else -1
            self.df['qty_equal_file'] = len(re.findall('[=]', file)) if len(file) != 0 else -1
            self.df['qty_at_file'] = len(re.findall('[@]', file)) if len(file) != 0 else -1
            self.df['qty_and_file'] = len(re.findall('[&]', file)) if len(file) != 0 else -1
            self.df['qty_exclamation_file'] = len(re.findall('[!]', file)) if len(file) != 0 else -1
            self.df['qty_space_file'] = len(re.findall('[ ]', file)) if len(file) != 0 else -1
            self.df['qty_tilde_file'] = len(re.findall('[~]', file)) if len(file) != 0 else -1
            self.df['qty_comma_file'] = len(re.findall('[,]', file)) if len(file) != 0 else -1
            self.df['qty_plus_file'] = len(re.findall('[+]', file)) if len(file) != 0 else -1
            self.df['qty_asterisk_file'] = len(re.findall('[*]', file)) if len(file) != 0 else -1
            self.df['qty_hashtag_file'] = len(re.findall('[#]', file)) if len(file) != 0 else -1
            self.df['qty_dollar_file'] = len(re.findall('[$]', file)) if len(file) != 0 else -1
            self.df['qty_percent_file'] = len(re.findall('[%]', file)) if len(file) != 0 else -1
            self.df['file_length'] = len(file) if len(file) != 0 else -1

            
            
            # Parameters
            
            

            if (len(url.fragment) == 0):
                parameter = url.query_string     # query_string  gives us entire parameters as string
            elif (len(url.fragment) > 0):
                parameter = url.query_string + '#' + url.fragment
                
            
            self.df['qty_dot_params'] = len(re.findall('[.]', parameter)) if len(parameter) != 0 else -1
            self.df['qty_hyphen_params'] = len(re.findall('[-]', parameter)) if len(parameter) != 0 else -1
            self.df['qty_underline_params'] = len(re.findall('[_]', parameter)) if len(parameter) != 0 else -1
            self.df['qty_slash_params'] = len(re.findall('[/]', parameter)) if len(parameter) != 0 else -1
            self.df['qty_questionmark_params'] = len(re.findall('[?]', parameter)) if len(parameter) != 0 else -1
            self.df['qty_equal_params'] = len(re.findall('[=]', parameter)) if len(parameter) != 0 else -1
            self.df['qty_at_params'] = len(re.findall('[@]', parameter)) if len(parameter) != 0 else -1
            self.df['qty_and_params'] = len(re.findall('[&]', parameter)) if len(parameter) != 0 else -1
            self.df['qty_exclamation_params'] = len(re.findall('[!]', parameter)) if len(parameter) != 0 else -1
            self.df['qty_space_params'] = len(re.findall('[ ]', parameter)) if len(parameter) != 0 else -1
            self.df['qty_tilde_params'] = len(re.findall('[~]', parameter)) if len(parameter) != 0 else -1
            self.df['qty_comma_params'] = len(re.findall('[,]', parameter)) if len(parameter) != 0 else -1
            self.df['qty_plus_params'] = len(re.findall('[+]', parameter)) if len(parameter) != 0 else -1
            self.df['qty_asterisk_params'] = len(re.findall('[*]', parameter)) if len(parameter) != 0 else -1
            self.df['qty_hashtag_params'] = len(re.findall('[#]', parameter)) if len(parameter) != 0 else -1
            self.df['qty_dollar_params'] = len(re.findall('[$]', parameter)) if len(parameter) != 0 else -1
            self.df['qty_percent_params'] = len(re.findall('[%]', parameter)) if len(parameter) != 0 else -1
            self.df['params_length'] = len(parameter) if len(parameter) != 0 else -1
            
            #Checking if there is any top level domain in parameters
            
            if len(parameter) == 0:
                self.df["tld_present_params"] = -1
                
            else:
                self.df["tld_present_params"] = 1 if bool(tldextract.extract(parameter).suffix) else 0

            self.df["qty_params"] = len(url.query) if len(parameter) != 0 else -1
            
            
            # Defining Website parameters
            
            
            self.time_response()
            self.is_registered()
            self.resolved_ips()
            self.number_ns_mx_records()
            
            self.tls_ssl_certificate()


                   

 
        except urllib.error.URLError as e:
            print("I am socket error")   
            
            
            
        except Exception as e:

            
            print(e)

        
            
            
            
        
            
            
            
    
        
            
    
            
    
        
     
            
            
    
                    
        
