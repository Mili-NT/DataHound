# Project Overview
https://github.com/Mili-NT/DataHound
## Project Details:
- Name: **DataHound**
- Category: **Data Collection & Analysis**
- Creator: **Mili**
- Maintainers: **None*
## Project Purpose:
DataHound uses one of three methods to search for exposed/public File Transfer Protocol servers.
This tool searches for an open FTP port (21), and attempts to login using anonymous credentials.
It then collects all data and exfiltrates it to the local system.
DataHound can use shodan querying, masscan ip range scanning, or file input for address methods.
## Project Intent:
DataHound is primarily intended for Data Collection purposes, but can also be used in security engagements to test for exposed attack surface.
It is designed to run continously for a long period of time on a system with a large amount of storage space.
Because FTP servers regularly contain hundreds of gigabytes of data, exteneral hard drives are recommended.
## Current Features:
- Multithreaded
- Three search types
- Configuration files
- Full linux and windows compatibility
## Planned Features:
- Data caps
- File filtering
- Security mode (brute forcing non-anonymous logins)
- proxy collection for anonymizing connection attempts
## Project Insights:
- 4 Stars
- 1 Fork
- 13 Commits Across 1 Branch

