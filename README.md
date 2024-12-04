# dnshuffler
Create list of typo or phishing domains for blocking on corporate firewalls.

There's a lot of examples when actors register typosquatting domains, listening to 25,53,80,110,443,465,995 and other ports, waiting when somebody in company mistyped domain, and connected to adversarie's server. 

After [Certainly tool](https://github.com/happycakefriends/certainly) was introduced at [blackhat'24](https://www.blackhat.com/us-24/briefings/schedule/index.html#flipping-bits-your-credentials-are-certainly-mine-40040) the amount of such attacks raised. 

> Certainly - is a offensive security toolkit to capture large amounts of traffic in various network protocols in bitflip and typosquatting scenarios. The tool was built to support research on these topics...

Why not using [urlcrazy](https://github.com/urbanadventurer/urlcrazy) or [dnstwist](https://github.com/elceef/dnstwist)? Because they are offense-tools - focused on finding seversal best typosquattings. I need defence tool - focused on coverage and completeness. It also must be simple to review and modify, without unnecessary founctionality like DNS queries. 

So here is a small tool to generate typosquattings. You can use 6 methods to generate a list of your domain typos and block them on corporate FW. When some IT guy or developer mistyped your corporate domain, portentially evil domain won't be resolved and dangerous request won't be sent. 

```
python3 dnshuffler.py -d "example.com,example.net" -o shuffled_domains.txt

python3 dnshuffler.py -d 2-lvl-domain.lst -f csv -o shuffled_domains.csv

python3 dnshuffler/dnshuffler.py -d "tcsbank.ru" -m swap,neighbor

```

Also you can use 7-th method "homoglyph" and defend against phising attacks, by adding the list hosts file on endpoints sinkholing them and blocking such domain resolutions. Method disabled by default.

```
python3 dnshuffler.py -d "tcsbank.ru" -m neighbor,similar,omit,duplicate,swap,neighbor_duplicate,homoglyph
```

Requres [idna python](https://github.com/kjd/idna/) module for punycode non-us characters in domain:
```
1) Clone
https://github.com/nikallass/dnshuffler.git

2) Activate python virtual environment
cd dnshuffler
python3 -m venv .
source venv/bin/activate

3) Install requrements
pip3 install -r requirements.txt

4) Run tool
python3 dnshuffler.py

5) Deactivate python virtual environment
deactivate
```

