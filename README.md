

# [About]

	____________________________________
	
	WELCOME TO MY LOG PARSER PROGRAM

	Author 		: Kazim Anil Aydin
	Writed in 	: Python 3.9
	
	_____________________________________

## [Command-Line Arguments]

> File Name 	= Any Log File (Required) 	
> Group Type 	= 1: HTTP Status Code, 2: IP Address (Required) 	
> Sort Type 	= 1: Request count, 2: Request Count Percentage, 3: Transferred Bytes (Required) 
> Result Limit 	= Any Number, Greater Than 0 (Optional)

	
## [Format]

	python task1_code.py "File Name" "Group Type" "Sort Type" "Result Limit"

## [Sample usage]

> python task1_code.py apache_logs.txt 1 1 5

### Arguments

> File Name 	= apache_logs.txt  	
> Group Type 	= (1) HTTP Status Code
> Sort Type 	= (1) Request Count 	
> Result Limit 	= 5

