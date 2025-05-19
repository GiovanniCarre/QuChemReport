from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os
from docx.shared import Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import numpy as np

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

def set_cell_border(cell, **kwargs):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()

    tcBorders = tcPr.find(qn('w:tcBorders'))
    if tcBorders is None:
        tcBorders = OxmlElement('w:tcBorders')
        tcPr.append(tcBorders)

    for edge in ('top', 'bottom', 'start', 'end', 'insideH', 'insideV'):
        if edge in kwargs:
            edge_data = kwargs[edge]
            tag = qn('w:' + edge)
            element = tcBorders.find(tag)
            if element is None:
                element = OxmlElement('w:' + edge)
                tcBorders.append(element)
            for key in edge_data:
                element.set(qn('w:' + key), str(edge_data[key]))

def hideTableBorders(table) :
    for row in table.rows:
        for cell in row.cells:
            set_cell_border(
                cell,
                top={"val": "single", "sz": 0, "color": "FFFFFF", "space" : 0},
                bottom={"val": "single", "sz": 0, "color": "FFFFFF", "space" : 0},
                start={"val": "single", "sz": 0, "color": "FFFFFF", "space" : 0},
                end={"val": "single", "sz": 0, "color": "FFFFFF", "space" : 0}
            )

def display_vertical_lines(table, centralLines=True):
    for row in table.rows:
        for i, cell in enumerate(row.cells):
            if centralLines:
                set_cell_border(
                    cell,
                    start={"val": "single", "sz": 2, "color": "000000", "space" : 0},
                    end={"val": "single", "sz": 2, "color": "000000", "space" : 0}
                )
            elif i == 0:
                set_cell_border(cell,start={"val": "single", "sz": 2, "color": "000000", "space": 0})
            elif i == len(row.cells) - 1:
                set_cell_border(cell,end={"val": "single", "sz": 2, "color": "000000", "space" : 0})

def create_table(doc, t):
    table = doc.add_table(rows=len(t), cols=len(t[0]))
    table.style = 'Table Grid'
    for i in range(len(t)):
        row = table.rows[i]
        for j in range(len(t[i])):
            row.cells[j].text = str(t[i][j])
    hideTableBorders(table)
    return table


def set_all_cell_borders(table) :
    for row in table.rows:
        for cell in row.cells:
            set_cell_border(
                cell,
                top={"val": "single", "sz": 0, "color": "FFFFFF"},
                bottom={"val": "single", "sz": 0, "color": "FFFFFF"},
                start={"val": "single", "sz": 0, "color": "FFFFFF"},
                end={"val": "single", "sz": 0, "color": "FFFFFF"}
            )


def modify_table(table):
    table.autofit = False
    tbl = table._tbl
    tblPr = tbl.tblPr
    tblBorders = OxmlElement('w:tblBorders')
    for border_name in ['top', 'left', 'bottom', 'right']:
        border = OxmlElement(f'w:{border_name}')
        border.set(qn('w:val'), 'none')  # Bordure invisible
        border.set(qn('w:sz'), '0')
        border.set(qn('w:space'), '0')
        tblBorders.append(border)
    insideH = OxmlElement('w:insideH')
    insideH.set(qn('w:val'), 'none')  # Bordure invisible
    insideH.set(qn('w:sz'), '0')
    insideH.set(qn('w:space'), '0')
    tblBorders.append(insideH)
    insideV = OxmlElement('w:insideV')
    insideV.set(qn('w:val'), 'single')  # Style de ligne
    insideV.set(qn('w:sz'), '12')  # Épaisseur (8 = standard, 12 = gras)
    insideV.set(qn('w:space'), '0')
    insideV.set(qn('w:color'), '000000')  # Couleur noire
    tblBorders.append(insideV)
    tblPr.append(tblBorders)

def positionImage(doc, src, pos, size):
    paragraph = doc.add_paragraph()
    paragraph.alignment = pos  # ou RIGHT, LEFT
    run = paragraph.add_run()
    run.add_picture(src, width=Inches(size))

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
    tablepos = create_table(doc, [["", ""]])
    left_cell = tablepos.cell(0, 0)
    right_cell = tablepos.cell(0, 1)
    left_cell.paragraphs[0].add_run().add_picture("temp/img-TOPOLOGY.png", Pt(200))
    right_cell.paragraphs[0].add_run().add_picture("temp/img-TOPOLOGY_cam2.png", Pt(200))
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
    table = create_table(doc, t)
    table.columns[0].width = Pt(80);
    table.columns[1].width = Pt(400);
    display_vertical_lines(table, False)
    doc.add_paragraph()
    add_section_title(doc, "2. COMPUTATIONAL DETAILS")


    ### SECTION 2

    t = []
    software = data_ref["comp_details"]["general"]["package"]
    try:
        t.append(['Software', data_ref["comp_details"]["general"]["package"], '(' + data_ref["comp_details"]["general"]["package_version"] + ')'])
    except KeyError:
        pass
    t.append(['Computational method', data_ref["comp_details"]["general"]["last_theory"], " "])
    t.append(['Functional', data_ref["comp_details"]["general"]["functional"], " "])
    try:
        t.append(['Basis set name', data_ref["comp_details"]["general"]["basis_set_name"], " "])
    except KeyError:
        pass
    t.append(['Number of basis set functions', data_ref["comp_details"]["general"]["basis_set_size"], " "])
    t.append(['Closed shell calculation', data_ref["comp_details"]["general"]["is_closed_shell"], " "])
    try:
        t.append(['Integration grid', data_ref["comp_details"]["general"]["integration_grid"], " "])
    except KeyError:
        pass
    try:
        t.append(['Solvent', data_ref["comp_details"]["general"]["solvent"], " "])
    except KeyError:
        pass
    #            TODO
    #            add_row_filter(param_table, ['Solvent reaction filed method',
    #                                         json_list[i]["comp_details"]["general"]["solvent_reaction_field"]])

    scfTargets = data_ref["comp_details"]["general"]["scf_targets"][-1]
    if software == "Gaussian":  # Gaussian or GAUSSIAN (upper/lower?
        t.append(["Requested SCF convergence on RMS and Max density matrix", scfTargets[0], scfTargets[1]])
        t.append(["Requested SCF convergence on energy", scfTargets[2], " "])
    if software == "GAMESS":
        t.append(["Requested SCF convergence on density", scfTargets[0], " "])

    # Specific calculations parameters :
    OPT_param_print = False
    for i, jsonfile in enumerate(json_list):
        # OPT calculation parameters :
        if ((job_types[i] == ['OPT']) or (job_types[i] == ['FREQ', 'OPT'])) and (OPT_param_print == False):
            t.append([" ", " ", " "])
            k = 0
            j = str(k + 1)
            try:
                t.append(["Job type: Geometry optimization", " ", " "])
                geomTargets = json_list[i]["comp_details"]["geometry"]["geometric_targets"]
                geomValues = json_list[i]["results"]['geometry']['geometric_values'][-1]
                if software == "Gaussian":  # Gaussian or GAUSSIAN (upper/lower?
                    t.append( ["Max Force value and threshold", "%.6f" % geomValues[0], "%.6f" % geomTargets[0]])
                    t.append(["RMS Force value and threshold", "%.6f" % geomValues[1], "%.6f" % geomTargets[1]])
                    t.append(["Max Displacement value and threshold", "%.6f" % geomValues[2], "%.6f" % geomTargets[2]])
                    t.append(["RMS Displacement value and threshold", "%.6f" % geomValues[3], "%.6f" % geomTargets[3]])
                    OPT_param_print = True  # to prevent repetition of data from OPT and FREQ
                if software == "GAMESS":
                    # in Hartrees per Bohr
                    t.append(["Max Force value and threshold", geomValues[0], geomTargets[0]])
                    t.append(["RMS Force value and threshold", geomValues[1], geomTargets[1]])
            except:
                pass
                # FREQ calculation parameters :
        if job_types[i] == ['FREQ'] or job_types[i] == ['FREQ', 'OPT'] or job_types[i] == ['FREQ', 'OPT', 'TD']:
            k = 0
            j = str(k + 1)
            t.append(["Job type: Frequency and thermochemical analysis", " ", " "])
            try:
                t.append(['Temperature', "%.2f K" % json_list[i]["comp_details"]["freq"]["temperature"], "  "])
            except:
                pass
            T_len = False
            try:
                len(json_list[i]["comp_details"]["freq"]["temperature"])
            except KeyError:
                json_list[i]["comp_details"]["freq"]["temperature"] = []
            except TypeError:
                T_len = True
                if T_len is True:
                    try:
                        t.append(['Anharmonic effects', json_list[i]["comp_details"]["freq"]["anharmonicity"], "  "])
                    except KeyError:
                        pass
            if (json_list[i]["comp_details"]["freq"]["temperature"]) != []:
                try:
                    t.append(['Anharmonic effects', json_list[i]["comp_details"]["freq"]["anharmonicity"], "  "])
                except KeyError:
                    pass
                    # TD calculation parameters :
        if job_types[i] == ['TD'] or job_types[i] == ['FREQ', 'OPT', 'TD']:
            k = 0
            j = str(k + 1)
            t.append(["Job type: Time-dependent calculation", " ", " "])
            try:
                t.append(['Number of calculated excited states and spin state', json_list[i]["comp_details"]["excited_states"]["nb_et_states"], np.unique(json_list[i]["results"]["excited_states"]["et_sym"])])
            except KeyError:
                pass
        t.append([" ", " ", " "])

    table = doc.add_table(rows=1, cols=2)
    hideTableBorders(table)
    display_vertical_lines(table)
    table0 = create_table(table.rows[0].cells[0], t)
    doc.add_paragraph("\nJob type: Geometry optimization")
    t = [
        ["test"],
        ["test"],
        ["test"],
        ["test"]
    ]
    table1 = create_table(table.rows[0].cells[1], t)
    table.columns[0].width = Pt(400)
    table.columns[1].width = Pt(80)
    table1.columns[0].width = Pt(55)
    doc.save("test.docx")
