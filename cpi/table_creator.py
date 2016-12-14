from terminaltables import AsciiTable
from colorclass import Color
import controller


def table_creator(file_names):
    """ Create a table with comparison two output files """

    results_list = controller.compare_output(file_names)
    title = "Comparison Table"

    print "\nComparing file_names:"
    print "FILE 1 = %s\nFILE 2 = %s" % (file_names[0], file_names[1])
    print "\nNOTE:\nA raise in number of all events represent a decrease in "\
          "the \nperformance of the application. Therefore, the smallest the "\
          "\npercentage, the better the application performance.\n"

    table_data = [
        ['Event Name', 'File 1', 'File 2', 'Percentage']
    ]

    # populate the table, converting negative percentage to red.
    for entry in results_list:
        table_data.append(entry)

    compare_table = AsciiTable(table_data, title)
    compare_table.justify_columns = {1: 'right', 2: 'right', 3: 'right'}
    print compare_table.table

    return 0
