# Downloads files from http://ms-vnext.net/UpdateArchive/.
# Upon completing the download, the program will try to find the SHA1 hash of the downloaded file
# on https://support.microsoft.com.
# If it is found, it will report the file as TRUSTED, otherwise NON-TRUSTED.

import os
import re
import hashlib
import argparse
from requests_html import HTMLSession


def parse_source_website(website, search_term):
    """Parse the rows containing search_term from the source code of a website."""

    r = HTMLSession().get(website)

    # CSS selector used to find the row containing the KB/file
    return r.html.find('#updates-table > tbody > tr', containing=search_term)


def download_file(link):
    """Download a file and return its content."""

    print('Downloading file: ' + file_name)
    r = HTMLSession().get('http://ms-vnext.net/' + link)

    return r.content


def sha1_file(file):
    """Calculate SHA1 hash of a file."""

    return hashlib.sha1(file).hexdigest()


def save_file(content, path):
    """Save file to a path."""

    # Create the directories if they do not exists
    os.makedirs(os.path.dirname(path), exist_ok=True)
    print('Saving as file: ' + path)
    with open(path, 'wb') as f:
        f.write(content)


def find_version_from_title(title_text):
    """Use version from the title as folder name to avoid duplicate file names."""

    version_found = re.search('[vV]ersion ([.\\da-zA-Z]*)', title_text)
    if version_found:
        return 'v' + version_found.group(1)
    else:
        return ''


def find_build_from_title(title_text):
    """Use build from the title as folder name to avoid duplicate file names."""

    build_found = re.search('[bB]uild ([.\\da-zA-Z]*)', title_text)
    if build_found:
        return 'b' + build_found.group(1)
    else:
        return ''


def validate_trustworthiness(website, sha1_hash):
    """Find hash in the source code of a website."""

    ms = HTMLSession().get(website)
    return re.search(sha1_hash, str(ms.content), re.IGNORECASE)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Downloads files from http://ms-vnext.net/UpdateArchive/. '
                                                 'Upon completing the download, the program will try to find the SHA1 '
                                                 'hash of the downloaded file on https://support.microsoft.com. '
                                                 'If it is found, it will report the file as TRUSTED, '
                                                 'otherwise NON-TRUSTED.')
    parser.add_argument('KB', help='Knowledge Base number OR file name you want to download.', type=str)
    args = parser.parse_args()
    search_keyword = args.KB

    # Find out if it's a KB or file search
    if re.fullmatch('[\\d]*', search_keyword):
        file_filter = None
    else:
        file_filter = search_keyword

    print(f'Chosen KB/file: {search_keyword}')

    html_rows = parse_source_website('http://ms-vnext.net/UpdateArchive/', search_keyword)
    for row in html_rows:
        # Parse file properties from each row
        kb = row.find('.kb')[0].text
        title = row.find('td.title')[0].text
        version = find_version_from_title(title)
        build = find_build_from_title(title)
        file_names = [fn.text for fn in row.find('td.files > a', containing=file_filter)]
        hyperlinks = [hl.attrs['href'] for hl in row.find('td.files > a', containing=file_filter)]

        # Go through required files in a row
        for file_name, hyperlink in zip(file_names, hyperlinks):
            file_content = download_file(hyperlink)
            file_hash = sha1_file(file_content)

            # Alter the output file name if version or build found
            f_name, f_ext = os.path.splitext(file_name)
            file_path = os.path.join(os.getcwd(), 'KBs', version, build, f_name + f_ext)

            save_file(file_content, file_path)

            # Try to find the SHA1 hash from the downloaded file on the specified website
            hash_found = validate_trustworthiness('https://support.microsoft.com/?kbid=' + kb, file_hash)

            if hash_found:
                print(f'{file_name} can be TRUSTED.\n')
            else:
                print(f'{file_name} is NON-TRUSTED.\n')
