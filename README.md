# KB downloader
Downloads files from http://ms-vnext.net/UpdateArchive/.  
Upon completing the download, the program will try to find the SHA1 hash of the downloaded file on https://support.microsoft.com.  
If it is found, it will report the file as TRUSTED, otherwise NON-TRUSTED.  
Files are downloaded to `KBs` folder and are split into sub-directories according to version/build to avoid overwriting files.

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

## Example runs

```
>>> python downloader.py 3198389

Chosen KB/file: 3198389
Downloading file: Windows10.0-KB3198389-x64.msu
Saving as file: Windows10.0-KB3198389-x64.msu
Windows10.0-KB3198389-x64.msu can be TRUSTED.
```

```
>>> python downloader.py Windows10.0-KB3197099-x86.cab
Chosen KB/file: Windows10.0-KB3197099-x86.cab
Downloading file: Windows10.0-KB3197099-x86.cab
Saving as file: Windows10.0-KB3197099-x86-v1607.cab
Windows10.0-KB3197099-x86-v1607.cab is NON-TRUSTED.
```

