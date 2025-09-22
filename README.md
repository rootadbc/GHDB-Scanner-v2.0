## GHDB Scanner v2.0  
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

## How the Scan Works

When you run the GHDB Scanner, it doesn’t crawl your site directly. Instead, it leverages DuckDuckGo’s search index to find pages on your target domain that match each Google Hacking Database (GHDB) dork. For every dork in your CSV, the tool:

1. Constructs a **site-restricted query** combining your target domain and the dork.  
   Example:  
   ```
   site:example.com inurl:admin
   ```

2. Sends this query to DuckDuckGo via the `duckduckgo_search` API.

3. Receives a list of indexed URLs that satisfy both conditions—i.e., they reside under your target domain **and** match the GHDB pattern (such as `filetype:sql`, `intitle:"index of"`, etc.).

4. Records each matching URL into your results CSV with the format:
   ```
   dork,matched_url
   inurl:admin,https://example.com/admin/login.php
   ```

By reusing DuckDuckGo’s indexing and search operators, the scanner quickly surfaces potential exposures without directly crawling or hammering your own server.

License  
MIT · Author: [rootadbc](https://github.com/rootadbc)
