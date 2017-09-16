import zillow_web_scraper_client as client
#import socks
#import socket
#socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5, addr="127.0.0.1", port=9050)
#socket.socket = socks.socksocket
print client.get_property_by_zpid(56756073)
