import requests
from Tools.tools import headers

url = 'https://waimai.meituan.com/ajax/poilist?_token=eJx90kt3mkAYBuD/whaOwlwZdxLlpqJBUZKcLDBCIQaI' \
      'Mgqkp/+9QNLQuiibeeb2zTtz+CmcrYMwUuTmo5JwDc/CSFAG8oAIksCLZgZTLDMMqcxIs+Dl7zFGgYwkYX/eToTRE2VAog' \
      'A8twNu039SMCSSStCz9EXQECCpbYS91SwRYs7fi9FwWAZJGiSDNEz4JcgGL3k6jPM0HJa8hMWJkrR6r5tA/1meheXXsJUd' \
      'wkpojkg37REIA0lREWi2fxH2RB3hDXFHdEPSEfckN6Q91Y70hqyj+i+x3JHdUGlJ5JagJ+zZ5SXKDbu8pL0F7uKQNjpm3yS' \
      'fddtbkM+6bV7yWZf2bJMR1BO3D3psH7Rpg++HBUyVJta2neR/JhfNH9RsLJIfWaPQrpzXQlmWx7HnclF3/Wjt5ZdxHdZTz' \
      'Rnf3x8MlHq1AaCtDN9jugZpBON8XYqI2iCqJnvXdfUEHHkxvk8K4/RQ2XNtNZNfL7v0mISWaxObTKyKO/Y5XkSFN4dmLqPF' \
      'jwPZOI6Rbz3ELe1l9hF58PRo7mudX+ZpJosbzT/O9pq+05ixtcs7K/IfjXKM9WzluWA63bnabImYY8yueZIjP+drNTaHnCl' \
      '3pmjRywfFi4cHv55WJL6+Zd7UXJwS8AZ3jgbNYL58zIzyGphb/CZGc8/f0JofWLrEH2rlrBaR5lO6e8UrXeSBs1Q3a/2OE5p' \
      'gJhd+TQ0Ij1Ace7Zhmlj49RtQ+vVz'
params = {
    'classify_type': 'cate_all',
    'sort_type': '0',
    'price_type': '0',
    'support_online_pay': '0',
    'support_invoice': '0',
    'support_logistic': '0',
    'page_offset': '21',
    'page_size': '20',
    'mtsi_font_css_version': 'e405872c',
    'uuid': 'qOFEvmr4sSdQ_fMDzxW2KoR0Si7krq9lZ4VR1ILEJJsOwT8erezKgrX-92IF5j2z',
    'platform': '1',
    'partner': '4',
    'originUrl': 'https%3A%2F%2Fwaimai.meituan.com%2Fhome%2Fwtw3sq76mxpy'
}
headers['Referer'] = 'https://waimai.meituan.com/home/wtw3sq76mxpy'
res = requests.post(url, data=params, headers=headers, verify=False).text
print(res)

