import re
s = "reload_allcogs\nhttps://discordapp.com/channels/296202585453363200/356095697428414477/651380976898801702 awe"
pattern = r"discordapp.com/channels/\d+/\d+/\d+"
a = re.findall(pattern, s)
print(a)
/296202585453363200/356095697428414477/651385118564548619
id: 651385118564548619
name: 648675794943475713