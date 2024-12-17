import argparse
from urllib.parse import urlparse, parse_qs, urlencode

def parse_url(url):
    parsed_url = urlparse(url.strip())
    query = parse_qs(parsed_url.query)
    return query

def extract_and_format_urls(urls):
    seen_params = set()
    formatted_urls = []

    for url in urls:
        parsed_url = urlparse(url.strip())
        query = parse_qs(parsed_url.query)
        query_tuple = tuple((k, tuple(v)) for k, v in sorted(query.items()))

        if query_tuple not in seen_params:
            seen_params.add(query_tuple)
            netloc = parsed_url.netloc if parsed_url.netloc else parsed_url.path.split('/')[0]
            path = parsed_url.path
            formatted_url = f"https://{netloc}{path}"
            if query:
                formatted_url += f"?{urlencode(query, doseq=True)}"
            formatted_urls.append(formatted_url)

    return formatted_urls

def read_urls_from_file(input_file):
    with open(input_file, 'r') as file:
        urls = file.readlines()
    return urls

def write_urls_to_file(output_file, formatted_urls):
    with open(output_file, 'w') as file:
        for url in formatted_urls:
            file.write(url + '\n')

def main():
    parser = argparse.ArgumentParser(description="Process and format a list of URLs.")
    parser.add_argument('-l', '--list', required=True, help="Path to the input file containing the list of URLs.")
    parser.add_argument('-o', '--output', required=True, help="Path to the output file to write the formatted URLs.")
    
    args = parser.parse_args()
    
    urls = read_urls_from_file(args.list)
    formatted_urls = extract_and_format_urls(urls)
    write_urls_to_file(args.output, formatted_urls)

if __name__ == "__main__":
    main()
