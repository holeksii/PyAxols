from pyaxols.atypes.table import Table
import xml.etree.ElementTree as ET


def write_xml(filepath: str, table: Table, encoding="utf-8") -> None:
    """Write a Table to an XML file.

    Args:
        filepath (str): The path to the file to write to.
        table (Table): The Table to write.
    """

    root = ET.Element("table")

    for i in range(table.shape[1]):
        row = ET.SubElement(root, "row")
        for j in range(table.shape[0]):
            ET.SubElement(row, table.cols[j]).text = str(table.i(i)[j])

    tree = ET.ElementTree(root)
    ET.indent(tree, space="    ")
    tree.write(filepath, encoding=encoding, xml_declaration=True)


def read_xml(filepath: str, encoding="utf-8") -> Table:
    """Read an XML file into a Table.

    Args:
        filepath (str): The path to the file to read from.

    Returns:
        Table: The Table read from the file.
    """
    tree = ET.parse(filepath)
    root = tree.getroot()

    cols = []
    for child in root[0]:
        cols.append(child.tag)

    empt = Table.empty(cols, tuple(str for _ in range(len(cols))))

    for child in root:
        row = []
        for subchild in child:
            row.append(subchild.text)
        empt.append_row(row)

    return empt
