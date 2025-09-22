GHDB Scanner v2.0  
Google Hacking Database Reconnaissance Tool

A hacker-themed CLI utility that automates site-restricted searches using the Google Hacking Database (GHDB) dorks. Leverages DuckDuckGo’s search API to scan any target domain for potential exposures, with real-time progress bars, timestamped logging, and CSV export.  

Features  
- Interactive prompts for target URL and dork list  
- Real DuckDuckGo site:<target> queries via `duckduckgo_search`  
- Configurable rate-limit delay and result count  
- Matrix-green banner, colorized status messages, and progress bars  
- URL validation, file checks, and ethical use warnings  

Usage  
1. Clone and install dependencies:  
   ```bash  
   git clone https://github.com/rootadbc/ghdb-scanner.git  
   cd ghdb-scanner  
   pip install -r requirements.txt  
   ```
2. Run the scanner:  
   ```bash  
   python ghdb_scanner_final.py  
   ```
   Follow the prompts to enter your target and GHDB CSV file.  

License  
MIT · Author: [rootadbc](https://github.com/rootadbc)
