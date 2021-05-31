#!/usr/bin/env python
# coding: utf-8

import sys
import re

init = dict(
	result_limit = None,
	sort_type = 1,
	group_type = 1,
	bypassed_parser_error = True,
)

#	result_limit =>				(Any Positive Number) => Default Value: None
#	sort_type =>				(1 => sort by request count, 2 => sort by request count percentage, 3 => sort by transferred bytes) => Default Value: 1
#	group_type => 				(1 => group by HTTP status code, 2 => group by IP address) => Default Value: 1
#	bypassed_parser_error => 	(True, False) => Default Value: True

result_limit = init['result_limit']

def is_intstring(_stringnumber):
	try:
		int(_stringnumber)
		return True
	except ValueError:
		return False

def print_group_types():
	_group_types = ['HTTP Status Code', 'IP Address']

	print('\n[CHOOSE AN OPTION FOR GROUP SELECTION]', end='\n \n')

	for index, group_type in enumerate(_group_types):
		print('{0}: Group By {1}'.format(index + 1, group_type))

def print_sort_types():
	_sort_types	= ['Request count', 'Request count percentage of all logged requests', 'Total number of bytes transferred'] 

	print('\n[CHOOSE AN OPTION FOR SORT AND PRINT SELECTION]', end='\n \n')

	for index, sort_type in enumerate(_sort_types):
		print('{0}: Sort By {1}'.format(index + 1, sort_type))

def print_help():
	###
	#
	# HELP SCREEN
	#
	###

	print('''
[About]

	WELCOME TO MY HTTP LOG PARSER PROGRAM

	Author 		: Kazim Anil Aydin
	Writed in 	: Python 3.9
	'''
	, end='\n')

	print('''
[Command-Line Arguments]

	File Name 	= Any Log File (Required)
	Group Type 	= 1: HTTP Status Code, 2: IP Address (Required)
	Sort Type 	= 1: Request count, 2: Request Count Percentage, 3: Transferred Bytes (Required)
	Result Limit 	= Any Number, Greater Than 0 (Optional)
	'''
	, end='\n')

	print('''
[Format]

	python task1_code.py "File Name" "Group Type" "Sort Type" "Result Limit"

[Sample usage]

	python task1_code.py apache_logs.txt 1 1 5

	- Arguments -

	File Name 	= apache_logs.txt 
	Group Type 	= (1) HTTP Status Code
	Sort Type 	= (1) Request Count
	Result Limit 	= 5
	'''
	, end='\n')

	exit()

def get_arguments():
	arguments = sys.argv
	argument_length = len(arguments)

	# Arguments ==>
	#	0 'Python Script Name'
	#	1 'File Name'
	#	2 '(1: HTTP Status Code, 2: IP Address)'
	#	3 '(1: Request count, 2: Request Count Percentage, 3: Transferred Bytes)'
	#	4 'Result Limit'

	if argument_length >= 1 and argument_length < 6:
		if argument_length == 1:
			# File Path Argument Required
			return 'File path argument is required', ()

		if argument_length == 2:
			if arguments[1] == 'help':
				print_help()
			# Group Type Argument Required
			print_group_types()
			return '\nCheck the "Group Type" value from the list above! Group type argument is required', ()

		if argument_length == 3:
			# Sort Type Argument Required
			print_sort_types()
			return '\nCheck the "Sort Type" value from the list above! Sort type argument is required', ()	

		file_name = arguments[1]
		group_type = arguments[2]
		sort_type = arguments[3]

		if argument_length > 4:
			result_limit = arguments[4]
			if is_intstring(result_limit):
				if int(result_limit) < 0:
					return 'Result limit must not be negative value', ()
				if int(result_limit) == 0:
					return 'Result limit must not be zero', ()
				init.update({'result_limit': int(result_limit)})
			else:
				return 'Result limit must be a number', ()
		

		if not (group_type in ['1', '2']):
			print_group_types()
			return '\nCheck the "Group Type" value from the list above! Your "Group Type" selection could not be found', ()
		
		if not (sort_type in ['1', '2', '3']):
			print_sort_types()
			return '\nCheck the "Sort Option" value from the list above! Your "Sort Option" selection could not be found', ()

		init.update({'sort_type': int(sort_type)})
		init.update({'group_type': int(group_type)})

		return False, (file_name, init['result_limit'])
	else:
		return 'It has many arguments', () 


def file_to_list(_filename):
	lines = []

	try:
		log_file = open(_filename, 'r').readlines()

		if len(log_file) < 1:
			return 'Empty log file detected!', lines

		for log_line in log_file:
			lines.append(log_line)

		return False, lines

	except FileNotFoundError:
		_err = 'File: "' + _filename + '" could not found!'
		return _err, lines

def log_parser(_lines):
	parts = [
		r'(?P<ip>\S+)',                 
		r'\S+',                     
		r'(?P<user>\S+)',          
		r'\[(?P<time>.+)\]',         
		r'"(?P<request>.*)"',      
		r'(?P<status_code>[0-9]+)',        
		r'(?P<size>\S+)',         
		r'"(?P<referrer>.*)"',
		r'"(?P<user_agent>.*)"',    
	]

	pattern = re.compile(r'\s+'.join(parts)+r'\s*\Z')

	parsed_log_data = []
	pattern_error_list = []

	for index, line in enumerate(_lines):
		line_number = index + 1
		try:
			data = pattern.match(line).groupdict()
			parsed_log_data.append(data)
		except:
			_err = 'Pattern error on this line {0}: '.format(line_number) + line
			pattern_error_list.append(_err)

			if init['bypassed_parser_error'] == False:
				print('Pattern error occured on this line {0}. Log file format is incorrect!'.format(line_number))
				exit()
				return

	if len(pattern_error_list) < 1:
		print('Log file format is correct! (No error occurred)')
		_err = False
	else:
		_err = '{0} incorrect patterns were found'.format(len(pattern_error_list))

	# print('Parsing has completed')
	# print('Line count: ' + str(len(parsed_log_data)))

	return _err, parsed_log_data, pattern_error_list

def group_log_data(_parsed_log):
	# Group the logged requests by IP address or HTTP status code (selected by user).

	grouped_by_option = dict()

	for log in _parsed_log:
		
		group_option = init['group_type']

		if group_option == 1:
			# group by HTTP Status Code
			group_key = log['status_code']
		else:
			# group by IP Address
			group_key = log['ip']
 
		# Group by Option
		if group_key in grouped_by_option:
			grouped_by_option[group_key].append(log)
		else:
			grouped_by_option[group_key] = list()
			grouped_by_option[group_key].append(log)

	return False, grouped_by_option

def calculate_log_data(_grouped_log, _total_parsed_log_count):
	# Calculate one of the following (selected by user) for each group:
	# 	Request count
	# 	Request count percentage of all logged requests
	# 	Total number of bytes transferred

	calculated_by_option = dict()
	total_request = 0

	for key_status_code in _grouped_log:
			
		request_count = 0
		request_count_percentage = 0
		total_number_of_bytes_transferred = 0
		
		for _log in _grouped_log[key_status_code]:
			request_count = request_count + 1

			size = 0
			
			if _log['size'] != '-':
				if is_intstring(_log['size']):
					size = int(_log['size'])

			total_number_of_bytes_transferred = total_number_of_bytes_transferred + size
		
		request_count_percentage = (request_count / _total_parsed_log_count) * 100

		calculated_by_option[key_status_code] = {
			'request_count': request_count,
			'request_count_percentage': request_count_percentage,
			'total_number_of_bytes_transferred': total_number_of_bytes_transferred
		}

	return False, calculated_by_option

def order_log(_calculated_log):
	# Print the results in descending order.
		#  Note: order the results by values described in (2), not by IP address or HTTP code.

	default_sort_type = 1 # Request Count
	sort_keys = ['request_count', 'request_count_percentage', 'total_number_of_bytes_transferred']

	sort_key = sort_keys[default_sort_type - 1]

	if is_intstring(init['sort_type']):
		if init['sort_type'] <= len(sort_keys) and init['sort_type'] > 0:
			sort_key = sort_keys[init['sort_type'] - 1]
	
	sorted_by_option = dict(sorted(_calculated_log.items(), key=lambda item: item[1][sort_key], reverse=True))

	return False, sorted_by_option

def print_result(_ordered_log, _max_printed_result = None):
	print('\n[RESULT]', end='\n \n')

	if _max_printed_result == None:
		_max_printed_result = len(_ordered_log)

	for i, key in enumerate(_ordered_log):
		if i + 1 > int(_max_printed_result):
			break

		report_data = _ordered_log[key]
		request_count, request_count_percentage, total_number_of_bytes_transferred = report_data.values()

		# default option
		# by HTTP Status Code 
		print_option = init['group_type']
		sort_type 	= init['sort_type']

		if print_option == 1:
			# by HTTP Status Code
			if sort_type == 1:
				print('HTTP Status Code: {0} Request count: {1}'.format(key, request_count))
			elif sort_type == 2:				
				print('HTTP Status Code: {0} Request count percentage of all logged requests: %{1:0.2f}'.format(key, request_count_percentage))
			elif sort_type == 3:
				print('HTTP Status Code: {0} Total number of bytes transferred: {1} byte'.format(key, total_number_of_bytes_transferred))
		else:
			# by IP Address
			if sort_type == 1:
				print('Ip Address: {0} Request count: {1}'.format(key, request_count))
			elif sort_type == 2:
				print('Ip Address: {0} Request count percentage of all logged requests: %{1:0.2f}'.format(key, request_count_percentage))
			elif sort_type == 3:
				print('Ip Address: {0} Total number of bytes transferred: {1} byte'.format(key, total_number_of_bytes_transferred))

def main():
	lines = []

	_error, args = get_arguments()

	if _error:
		# GET ARGUMENTS SECTION
		print(_error) # An Error Occurred
		return
	else:
		# READ FILE SECTION
		_error, log = file_to_list(args[0])
		result_limit = args[1]

		if _error:
			print(_error) # An Error Occurred
			return
		else:
			# LOG PARSER SECTION
			_error, parsed_log, pattern_errors = log_parser(log)

			if _error:
				# PATTERN ERROR SECTION
				print(_error) # An Error Occurred
				if len(pattern_errors) > 0:
					list(map(print, pattern_errors))

			_error, grouped_log = group_log_data(parsed_log)

			if _error:
				# LOG GROUP SECTION
				print(_error)  # An Error Occurred
				return
			else:
				# LOG CALCULATE SECTION
				_error, calculated_log = calculate_log_data(grouped_log, len(parsed_log))

				if _error:
					print(_error)  # An Error Occurred
					return
				else:
					# LOG SORT AND PRINT RESULT SECTION
					_error, ordered_log = order_log(calculated_log)

					print_result(ordered_log, result_limit)

if __name__ == '__main__':
	main()