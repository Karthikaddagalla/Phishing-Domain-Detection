import pandas as pd
import numpy as np
import re

df = pd.read_csv("code_files/dataset_small.csv")

# After examinig the dataset, we are going to remove unnecessary columns


new_df = df.drop([ 
 'qty_exclamation_url','qty_space_url','qty_tilde_url','qty_comma_url','qty_plus_url',
 'qty_asterisk_url','qty_hashtag_url','qty_dollar_url','qty_percent_url',
 
 
 'qty_slash_domain','qty_questionmark_domain','qty_equal_domain',
 'qty_and_domain','qty_exclamation_domain','qty_space_domain','qty_tilde_domain',
'qty_comma_domain','qty_plus_domain','qty_asterisk_domain','qty_hashtag_domain',
 'qty_dollar_domain','qty_percent_domain',
 

 'qty_redirects', 'url_google_index','domain_google_index', 
 'url_shortened', 'domain_spf', 'asn_ip'


 ], axis = 1)

# We are doing these because it should be an boolean with 0 and 1 but there are -1 values in dataset.
new_df["tld_present_params"].replace(-1, 0, inplace = True)  

print(new_df["tld_present_params"].value_counts())
print(len(new_df.columns))