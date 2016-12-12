from terminaltables import AsciiTable
import controller


def table_creator(file_names):
    """ Create a table with comparison two output files """

    results_list = controller.compare_output(file_names)

    print "Comparing file_names: %s and %s" % (file_names[0], file_names[1])

    table_data = [
        ['EVENT NAME', 'VALUE', 'VALUE', '%'],
    ]

    for entry in results_list:
        table_data.append(entry)

    compare_table = AsciiTable(table_data)
    print compare_table.table

    return 0
