import random
PROXY_LIST= [
	'120.194.73.8:8088',
	'117.146.116.69:80',
	'115.218.178.225:8888',
	'183.223.177.184:8123',
	'183.140.160.113:80',
	'111.248.87.94:8088',
	'117.69.22.191:8088',
	'223.86.41.203:8123',
	'111.11.228.10:80',
	'183.207.229.140:8090',
	'42.51.4.25:80',
	'27.224.203.252:8088',
]
class RandomProxyMiddleware(object):
	def process_request(self, request, spider):
		#request.meta['proxy'] = "http://YOUR_PROXY_IP:PORT"
   		po = random.choice(PROXY_LIST)
		if po :
			request.meta['proxy'] = "http://%s" % po
		# Use the following lines if your proxy requires authentication 
		#proxy_user_pass = "USERNAME:PASSWORD"
		# setup basic authentication for the proxy 
		#encoded_user_pass = base64.encodestring(proxy_user_pass) 
		#request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
