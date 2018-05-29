#!/usr/bin/env python3

import logging
import argparse
import pandas
import matplotlib


def get_students_at():
    """
    Reads the total number of students in the winter terms in Austria.
    Data source: https://www.data.gv.at/katalog/dataset/66453c59-ae4b-37b6-80d4-25dfeeab1376
    :return: A panda series <WS<yy>, <number-of-students>>
    """

    # Convert the number of students to int
    data_converters = {'F-STUD_PERS': lambda x: int(float(x.replace(',', '.')))}

    # Convert the winter term name to the short version "WSXX"
    header_converters = {'name': lambda x: x.replace('Wintersemester 20', 'WS')[:-3]}

    # Load (and convert) the data
    logging.debug('Reading Austrian statistics.')
    data_url = 'http://data.statistik.gv.at/data/OGD_unistud2_ext_UNI_STUD2_1.csv'
    data_at = pandas.read_csv(filepath_or_buffer=data_url, sep=';', converters=data_converters)
    term_names_url = 'http://data.statistik.gv.at/data/OGD_unistud2_ext_UNI_STUD2_1_C-SEMESTER-0.csv'
    term_names_at = pandas.read_csv(filepath_or_buffer=term_names_url, sep=';', converters=header_converters)
    merged = data_at.merge(term_names_at, left_on='C-SEMESTER-0', right_on='code', how='left')

    # Only keep term and number of students
    winter_terms_at = merged.filter(items=['name', 'F-STUD_PERS'])
    winter_terms_at.columns = ['term', 'Students in Austria']
    # Filter for winter terms
    winter_terms_at = winter_terms_at[winter_terms_at['term'].str.contains('WS')]

    # Group by the semester and sum up the number of students
    winter_terms_at = winter_terms_at.groupby(['term'])['Students in Austria'].agg('sum')

    logging.debug('Students in the winter term in Austria:')
    logging.debug(winter_terms_at)
    logging.debug(type(winter_terms_at))

    return winter_terms_at


def get_students_de():
    """
    Reads the total number of students in the winter terms in Germany.
    Data source: https://www.govdata.de/web/guest/suchen/-/details/de-bmbf-datenportal-tabelle-2_5_23
    :return: A panda series <WS<yy>, <number-of-students>>
    """
    data_url = 'http://www.datenportal.bmbf.de/portal/en/Table-2.5.23.csv'
    # Load the CSV
    winter_terms_de = pandas.read_csv(filepath_or_buffer=data_url, sep=',', encoding='latin1')
    # Select the total number of students (including foreigners) between WS03 and WS16
    winter_terms_de = winter_terms_de[62:76].iloc[:,2:4]
    # Name the columns as in the data-set of Austria
    winter_terms_de.columns = ['term', 'Students in Germany']
    # Convert the number to int
    winter_terms_de['Students in Germany'] = winter_terms_de['Students in Germany'].astype(int)
    # Convert the term name to the short version (WS<yy>)
    winter_terms_de['term'] = winter_terms_de['term'].str[:-5]
    winter_terms_de['term'] = winter_terms_de['term'].str.replace('20', 'WS')
    # Create a series
    winter_terms_de = winter_terms_de.groupby(['term'])['Students in Germany'].agg('sum')
    logging.debug('Students in the winter term in Germany:')
    logging.debug(winter_terms_de)
    return winter_terms_de


def main():
    parser = argparse.ArgumentParser(
        description='')
    parser.add_argument('-v', '--verbose',
                        help="Sets the log level to DEBUG",
                        action="store_true")
    parser.add_argument('-p', '--plot',
                        help="Open a windows showing the plot (not supported when executed in docker)",
                        action="store_true")
    args = parser.parse_args()
    if args.verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logging.basicConfig(level=log_level, format='%(asctime)s %(levelname)s %(message)s')

    # Get the data
    data_at = get_students_at()
    data_de = get_students_de()

    # Combine the series to a data frame
    combined = pandas.concat([data_at, data_de], axis=1)

    # Save the data frame as CSV
    combined.to_csv('output/data.csv')

    # If the plot is not shown, switch to the 'agg' matplotlib
    # backend to allow creating plots without an x server
    if not args.plot:
        matplotlib.use('agg')
    import matplotlib.pyplot as plot

    # Plot the data frame
    combined.plot.bar()

    # Save the image of the plot
    plot.savefig('output/students.png')
    # If the argument --plot has been set, show the plot in a window
    if args.plot:
        plot.show()


if __name__ == "__main__":
    main()
