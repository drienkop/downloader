# KB downloader
Downloads files from http://ms-vnext.net/UpdateArchive/.  
Upon completing the download, the program will try to find the SHA1 hash of the downloaded file on https://support.microsoft.com.  
If it is found, it will report the file as TRUSTED, otherwise NON-TRUSTED.

## Minimum Python version
3.6.6

## How to run
```
>>> python downloader.py -h
usage: downloader.py [-h] KB

positional arguments:
  KB          Knowledge Base number OR file name you want to download.

optional arguments:
  -h, --help  show this help message and exit
```

## Example run

```
>>> python downloader.py 3198389

Chosen KB/file: 3198389
Downloading file: Windows10.0-KB3198389-x64.msu
Saving as file: Windows10.0-KB3198389-x64.msu
Windows10.0-KB3198389-x64.msu can be TRUSTED.
```

