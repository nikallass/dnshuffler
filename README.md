# dnshuffler
Create list of typo or phish domains for blocking on corporate firewalls

There's a lot of examples when actors register squatting domains, listening to 25,53,80,110,443,465,995 and other ports, waiting when somebody in company mistyped domain, and connected to adversarie's server. 

After [Certainly tool](https://github.com/happycakefriends/certainly) was introduced on [blackhat'24](https://www.blackhat.com/us-24/briefings/schedule/index.html#flipping-bits-your-credentials-are-certainly-mine-40040) the amount of such attacks raised. 

> Certainly - is a offensive security toolkit to capture large amounts of traffic in various network protocols in bitflip and typosquat scenarios. The tool was built to support research on these topics...

You can use 5 methods to generate a list of your domain typos and block them on corporate FW. When some IT guy or developer mistyped your corporate domain, portentially evil domain won't be resolved and dangerous request won't be sent. 

```
python3 dnshuffler.py -d "example.com,example.net" -o shuffled_domains.txt

python3 dnshuffler.py -d 2-lvl-domain.lst -f csv -o shuffled_domains.csv

python3 dnshuffler/dnshuffler.py -d "tcsbank.ru" -m swap neighbor

```

