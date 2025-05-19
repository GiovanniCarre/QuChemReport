from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os
from docx.shared import Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def add_section_title(doc, title_text):
    p = doc.add_paragraph()
    run = p.add_run(title_text)
    run.bold = True
    run.font.size = Pt(14)
    run.font.color.rgb = RGBColor(255, 255, 255)
    p_format = p.paragraph_format
    p_format.space_after = Pt(6)

    shading_elm = OxmlElement('w:shd')
    shading_elm.set(qn('w:fill'), '008080')  # Vert canard
    p._element.get_or_add_pPr().append(shading_elm)

def create_table(doc, t):
    table = doc.add_table(rows=len(t), cols=2)
    table.style = 'Table Grid'
    for i in range(len(t)):
        row = table.rows[i]
        print("row", row)
        row.cells[0].text = str(t[i][0])
        row.cells[1].text = str(t[i][1])

def json2docx(config, json_list, data, mode="clean"):
    report_type = config.output.include.electron_density_difference.mode
    data_ref = data['data_for_discretization']
    job_types = data['job_types']
    name = data_ref["molecule"]["formula"]
    dirname = os.path.basename(os.getcwd())
    doc = Document()
    title = doc.add_paragraph()
    run = title.add_run("MOLECULAR CALCULATION REPORT")
    run.bold = True
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph("")
    section_title = doc.add_paragraph()
    run = section_title.add_run("1. MOLECULE")
    run.bold = True
    run.font.size = Pt(14)
    section_title_format = section_title.paragraph_format
    section_title_format.space_after = Pt(6)
    doc.add_picture("temp/img-TOPOLOGY.png", width=Inches(1))
    doc.add_picture("temp/img-TOPOLOGY_cam2.png", width=Inches(3))
    last_paragraph = doc.paragraphs[-1]
    last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    caption = doc.add_paragraph("Figure 1: Chemical structure diagram with atomic numbering from two points of view.")
    caption.alignment = WD_ALIGN_PARAGRAPH.CENTER

    inchi = (data_ref["molecule"]["inchi"]).rstrip().split("=")[-1]
    t = [
        ["Directory name", dirname],
        ["Formula", data_ref["molecule"]["formula"]],
        ["Charge", data_ref["molecule"]["charge"]],
        ["Spin multiplicity", data_ref["molecule"]["multiplicity"]]]
    if report_type == 'full':
        t.append(["Monoisotopic mass", "%.5f Da" % data_ref["molecule"]["monoisotopic_mass"]])
        t.append(["InChI", inchi])
        if (len(data_ref["molecule"]["smi"]) < 80):
            t.append(["SMILES", data_ref["molecule"]["smi"]])
    create_table(doc, t)
    add_section_title(doc, "2. COMPUTATIONAL DETAILS")

    t = [
        ("Software", "Gaussian", "(2009+D.01)"),
        ("Computational method", "DFT", ""),
        ("Functional", "B3LYP", ""),
        ("Basis set name", "6-31G(d)", ""),
        ("Number of basis set functions", "19", ""),
        ("Closed shell calculation", "True", ""),
        ("Requested SCF convergence on RMS and Max density matrix", "1e-08", "1e-06"),
        ("Requested SCF convergence on energy", "1e-06", ""),
        ("Job type", "Time-dependent calculation", ""),
        ("Number of calculated excited states and spin state", "5",
         "['Singlet-A1', 'Singlet-A2', 'Singlet-B1', 'Singlet-B2']")
    ]
    create_table(doc, t)
    doc.add_paragraph("\nJob type: Geometry optimization")
    t = [
        ("Max Force value and threshold", "0.000156", "0.000450"),
        ("RMS Force value and threshold", "0.000101", "0.000300"),
        ("Max Displacement value and threshold", "0.000578", "0.001800"),
        ("RMS Displacement value and threshold", "0.000550", "0.001200")
    ]
    create_table(doc, t)

    doc.save("test.docx")