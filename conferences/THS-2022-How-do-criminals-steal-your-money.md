# How do criminals steal your money? A few words about online credit card skimmers. 

* Credit cards transaction in internet are dangeraus
  * Skimmer - phisical 
  * Online skimmer - use vulnerabilities to inject code to online shops -> selling those carts on darkweb
  * Magecart - many groups that are using advanced JavaScript code
  * Urlscan.io - way to find infected 
  * ![image](https://user-images.githubusercontent.com/17719543/195529442-c31f25f7-092d-4456-83b7-bddc5d9fa057.png)
  * ![image](https://user-images.githubusercontent.com/17719543/195529629-56ac67a3-40ae-4341-a691-92dfcf1f367e.png)
  * Check for indicator
  * There are some JavaScript loaded mostly from Polish IP, but there is one from Germany
  * Use attacker IP in Urlscan you can find more infected websites
* Online skimmer
  * It adds click listener to all buttons
  * On button click it's trying to get all inputs from forms
  * It need to get ride of real credit cart panel, and it adds it own payment panel
  * ![image](https://user-images.githubusercontent.com/17719543/195532677-29629cc6-48cb-43a3-9f7c-722800fc4751.png) 
  * Data is exfiltrated - as base64 -> base64 -> hex -> utf-16b
  * It's adding some random data to mask real one
  * Open HTTP connection and send data using POST
* Mitigations
  * One-time use credit-cards
  * Predpaid credit cards
  * Credit Card limits
  * Chargeback
* Inline payment panel are suspicious 
