# i6mA-vote
##############################################################

command:

	python main.py -i inputfile -o outputfile
	
example:

	python main.py -i ./examples.txt -o result.csv
	
##############################################################

1. Operating environment:

	python 3.9.7 + numpy 1.21.4 + pandas 1.3.4 + sklearn 1.0.1 + joblib 1.1.0 + xgboost 1.5.1


2. Download this program:

	As ./model.pkl are more than 100M, it is not its original file downloaded directly through "download zip".
	
	Therefore, after "download zip", you need to download the file separately to cover the content in the zip package.

3. Run the program:

	You can run the program with the following command:
	
		python main.py -i inputfile -o outputfile
	
	where main.py is the main file of the whole program, we rely on it to run and call other files;
	
	inputfile refers to the file containing DNA sequences in FASTA format with lengths greater than or equal to 41;
	
	outputfile denotes the result file output from our program and it is better to set this file in .CSV format for easy viewing.

4. If you have any questions, please contact me at zhaozhengnan@outlook.com
