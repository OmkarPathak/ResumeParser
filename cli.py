# Author: Omkar Pathak

import os
import argparse
from pprint import pprint
from resume_parser.resume_parser import ResumeParser
import multiprocessing as mp

def print_cyan(text):
    print("\033[96m {}\033[00m" .format(text))

class ResumeParserCli(object):
    def __init__(self):     
        self.__parser = argparse.ArgumentParser()
        self.__parser.add_argument('-f', '--file', help="resume file to be extracted")
        self.__parser.add_argument('-d', '--directory', help="directory containing all the resumes to be extracted")
        return

    def extract_resume_data(self):
        args = self.__parser.parse_args()

        if args.file and not args.directory:
            return self.__extract_from_file(args.file)
        elif args.directory and not args.file:
            return self.__extract_from_directory(args.directory)
        else:
            return 'Invalid option. Please provide a valid option.'

    def __extract_from_file(self, file):
        if os.path.exists(file):
            print_cyan('Extracting data from: {}'.format(file))
            resume_parser = ResumeParser(file)
            return [resume_parser.get_extracted_data()]
        else:
            return 'File not found. Please provide a valid file name.'

    def __extract_from_directory(self, directory):
        if os.path.exists(directory):
            pool = mp.Pool(mp.cpu_count())

            resumes = []
            data = []
            for root, directories, filenames in os.walk(directory):
                for filename in filenames:
                    file = os.path.join(root, filename)
                    resumes.append(file)

            results = pool.map(resume_result_wrapper, resumes)
            pool.close()
            pool.join()

            return results
        else:
            return 'Directory not found. Please provide a valid directory.'

def resume_result_wrapper(resume):
    print_cyan('Extracting data from: {}'.format(resume))
    parser = ResumeParser(resume)
    return parser.get_extracted_data()

if __name__ == '__main__':
    cli_obj = ResumeParserCli()
    pprint(cli_obj.extract_resume_data())