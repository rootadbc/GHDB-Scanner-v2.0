#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                          GHDB SCANNER v2.0                                  ║
║                     Google Hacking Database Tool                            ║
║                                                                              ║
║  Author: rootadbc                          Framework: Python 3.8+           ║
║         https://github.com/rootadbc                                          ║
║         https://www.linkedin.com/in/rootadbc/                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import csv
import argparse
from datetime import datetime
from urllib.parse import urlparse
from duckduckgo_search import DDGS

# Terminal color codes
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    MATRIX = '\033[38;5;46m'
    DARK_GREEN = '\033[38;5;22m'

def print_banner():
    """Display the hacker-style banner"""
    banner = f"""
{Colors.MATRIX}{Colors.BOLD}
    ██████╗ ██╗  ██╗██████╗ ██████╗     ███████╗ ██████╗ █████╗ ███╗   ██╗
    ██╔════╝ ██║  ██║██╔══██╗██╔══██╗    ██╔════╝██╔════╝██╔══██╗████╗  ██║
    ██║  ███╗███████║██║  ██║██████╔╝    ███████╗██║     ███████║██╔██╗ ██║
    ██║   ██║██╔══██║██║  ██║██╔══██╗    ╚════██║██║     ██╔══██║██║╚██╗██║
    ╚██████╔╝██║  ██║██████╔╝██████╔╝    ███████║╚██████╗██║  ██║██║ ╚████║
     ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═════╝     ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
{Colors.END}
{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════════════════╗
║                        Google Hacking Database Scanner                       ║
║                          Advanced Reconnaissance Tool                        ║
╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.END}
"""
    print(banner)

def print_divider():
    """Print a stylized divider"""
    print(f"{Colors.DARK_GREEN}{'═' * 80}{Colors.END}")

def print_status(status_type, message):
    """Print formatted status messages"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    if status_type == "info":
        print(f"{Colors.CYAN}[{timestamp}] [INFO]{Colors.END} {message}")
    elif status_type == "success":
        print(f"{Colors.GREEN}[{timestamp}] [SUCCESS]{Colors.END} {message}")
    elif status_type == "warning":
        print(f"{Colors.YELLOW}[{timestamp}] [WARNING]{Colors.END} {message}")
    elif status_type == "error":
        print(f"{Colors.RED}[{timestamp}] [ERROR]{Colors.END} {message}")
    elif status_type == "scan":
        print(f"{Colors.PURPLE}[{timestamp}] [SCAN]{Colors.END} {message}")

def print_target_info(target_url, dorks_file):
    """Display target information in hacker style"""
    print_divider()
    print(f"{Colors.BOLD}{Colors.WHITE}TARGET ACQUISITION{Colors.END}")
    print_divider()
    print(f"{Colors.CYAN}Target URL:{Colors.END} {Colors.WHITE}{target_url}{Colors.END}")
    print(f"{Colors.CYAN}Dorks File:{Colors.END} {Colors.WHITE}{dorks_file}{Colors.END}")
    print(f"{Colors.CYAN}Timestamp:{Colors.END} {Colors.WHITE}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")
    print(f"{Colors.CYAN}Status:{Colors.END} {Colors.GREEN}LOCKED ON{Colors.END}")
    print_divider()

def validate_inputs(target_url, dorks_file):
    """Validate user inputs"""
    errors = []
    
    # Validate URL
    try:
        parsed = urlparse(target_url)
        if not parsed.scheme or not parsed.netloc:
            errors.append("Invalid URL format. Please include http:// or https://")
    except Exception:
        errors.append("Invalid URL format")
    
    # Validate dorks file
    if not os.path.exists(dorks_file):
        errors.append(f"Dorks file not found: {dorks_file}")
    elif not dorks_file.lower().endswith('.csv'):
        errors.append("Dorks file must be a CSV file")
    
    return errors

def load_dorks_from_csv(file_path):
    """Load dorks from CSV file with error handling"""
    print_status("info", f"Loading dorks from {file_path}...")
    dorks = []
    
    try:
        with open(file_path, 'r', encoding='utf-8', newline='') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader, None)  # Skip header
            
            for row in reader:
                if row:  # Skip empty rows
                    dork = row[0].strip().strip('"')  # Remove quotes and whitespace
                    if dork:
                        dorks.append(dork)
        
        print_status("success", f"Loaded {len(dorks)} dorks from database")
        return dorks
        
    except FileNotFoundError:
        print_status("error", f"Dorks file not found: {file_path}")
        return []
    except Exception as e:
        print_status("error", f"Failed to load dorks: {str(e)}")
        return []

def scan_with_progress(target_url, dorks, max_results=20, delay=1.0):
    """Perform actual scanning via DuckDuckGo site-restricted searches"""
    print_divider()
    print(f"{Colors.BOLD}{Colors.RED}INITIATING VULNERABILITY SCAN{Colors.END}")
    print_divider()
    
    results = []
    total_dorks = len(dorks)
    
    # Create output filename
    hostname = urlparse(target_url).netloc.replace('.', '_')
    output_file = f"{hostname}_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    print_status("scan", f"Scanning {target_url} with {total_dorks} dorks")
    print_status("info", f"Results will be saved to: {output_file}")
    
    # Initialize DuckDuckGo search
    ddgs = DDGS()
    
    for i, dork in enumerate(dorks, 1):
        # Update progress bar
        percentage = (i / total_dorks) * 100
        progress_bar = "█" * int(percentage / 2) + "░" * (50 - int(percentage / 2))
        
        print(f"\r{Colors.PURPLE}[SCANNING] {Colors.WHITE}[{progress_bar}] {percentage:.1f}% | Dork #{i}/{total_dorks}{Colors.END}", end="")
        
        # Perform site-restricted search
        query = f"site:{urlparse(target_url).netloc} {dork}"
        
        try:
            search_results = ddgs.text(query, max_results=max_results)
            for result in search_results:
                url = result.get("href")
                if url:
                    results.append({
                        'dork': dork,
                        'url': url
                    })
        except Exception as e:
            # Silently continue on search errors to avoid cluttering output
            pass
        
        # Delay between requests
        time.sleep(delay)
    
    print(f"\n{Colors.GREEN}[✓] Scan sequence completed{Colors.END}")
    print_status("success", f"Found {len(results)} potential exposures")
    
    # Save results to CSV
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['dork', 'matched_url'])
            for result in results:
                writer.writerow([result['dork'], result['url']])
        
        print_status("success", f"Results saved to: {output_file}")
    except Exception as e:
        print_status("error", f"Failed to save results: {str(e)}")
    
    return results, output_file

def setup_argument_parser():
    """Setup command line argument parser"""
    parser = argparse.ArgumentParser(
        description="GHDB Scanner - Google Hacking Database Reconnaissance Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ghdb_scanner.py
        """
    )
    
    parser.add_argument('--delay', 
                       type=float, 
                       default=1.0,
                       help='Delay between requests in seconds (default: 1.0)')
    parser.add_argument('--max-results', 
                       type=int, 
                       default=20,
                       help='Maximum results per dork (default: 20)')
    
    return parser

def main():
    """Main execution function with hacker styling"""
    try:
        # Clear screen
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print_banner()
        
        # Warning message
        print(f"{Colors.RED}{Colors.BOLD}⚠️  WARNING: AUTHORIZED USE ONLY ⚠️{Colors.END}")
        print(f"{Colors.YELLOW}This tool is for ethical hacking and authorized penetration testing only.{Colors.END}")
        print(f"{Colors.YELLOW}Unauthorized use may violate laws and terms of service.{Colors.END}")
        print_divider()
        
        # Mission parameters section
        print(f"{Colors.BOLD}{Colors.WHITE}MISSION PARAMETERS{Colors.END}")
        print_divider()
        
        # Always prompt for target URL and dorks file
        target_url = input(f"{Colors.CYAN}Enter target URL (e.g., https://example.com): {Colors.WHITE}").strip()
        dorks_file = input(f"{Colors.CYAN}Enter path to dorks CSV file [default: ghdb_dorks.csv]: {Colors.WHITE}").strip()
        
        if not dorks_file:
            dorks_file = "ghdb_dorks.csv"
        
        print(f"{Colors.END}")
        
        # Validate inputs
        errors = validate_inputs(target_url, dorks_file)
        if errors:
            print_status("error", "Validation failed:")
            for error in errors:
                print(f"{Colors.RED}  ✗ {error}{Colors.END}")
            sys.exit(1)
        
        # Display mission parameters
        print_target_info(target_url, dorks_file)
        
        # Load dorks from CSV
        dorks = load_dorks_from_csv(dorks_file)
        if not dorks:
            print_status("error", "No dorks loaded. Exiting...")
            sys.exit(1)
        
        # Setup argument parser for optional parameters
        parser = setup_argument_parser()
        args = parser.parse_args()
        
        # Perform scan
        results, output_file = scan_with_progress(target_url, dorks, args.max_results, args.delay)
        
        # Mission complete
        print_divider()
        print(f"{Colors.GREEN}{Colors.BOLD}MISSION ACCOMPLISHED{Colors.END}")
        print(f"{Colors.WHITE}Target: {target_url}{Colors.END}")
        print(f"{Colors.WHITE}Dorks processed: {len(dorks)}{Colors.END}")
        print(f"{Colors.WHITE}Potential findings: {len(results)}{Colors.END}")
        print(f"{Colors.WHITE}Results saved to: {output_file}{Colors.END}")
        print_divider()
        
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!] Operation interrupted by user{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print_status("error", f"Critical error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()