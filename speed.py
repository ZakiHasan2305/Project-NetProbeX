
import speedtest
import inspect

s = speedtest.Speedtest()

#show what we can get
#for method in inspect.getmembers(s, predicate=inspect.ismethod):
 #print(method[0])

#Download Speed

print("My download speed is: ",s.download()/1000000)

#Upload Speed

print("My upload speed is: ",s.upload()/1000000)

#Best Server

best_server = s.get_best_server()
for key, value in best_server.items():
    print(key, ' : ', value)


#Closest Server

print("\n")

closest_server = s.get_closest_servers()
for key, value in closest_server[0].items():
    print(key, ' : ',value)

#All Servers
    
#print("\n")

#servers = s.get_servers()
#for key, value in servers.items():
 #   print(key, ' : ',value)


