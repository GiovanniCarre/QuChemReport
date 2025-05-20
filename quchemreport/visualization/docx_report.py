from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os
from docx.shared import Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import numpy as np

def add_section_title(doc, title_text):
    section = doc.sections[0]
    section.left_margin = Inches(0.6)
    section.right_margin = Inches(0.6)
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Pt(0)
    p.paragraph_format.right_indent = Pt(0)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run(title_text)
    run.bold = True
    run.font.size = Pt(14)
    run.font.color.rgb = RGBColor(255, 255, 255)
    shading_elm = OxmlElement('w:shd')
    shading_elm.set(qn('w:val'), 'clear')
    shading_elm.set(qn('w:color'), 'auto')
    shading_elm.set(qn('w:fill'), '009080')
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

def set_vertical_line(table, index, visible):
    color = "000000" if visible else "FFFFFF"
    for row in table.rows:
        if index == len(row.cells):
            set_cell_border(row.cells[index-1], end={"val": "single", "sz": 2, "color": color, "space": 0})
        else :
            set_cell_border(row.cells[index], start={"val": "single", "sz": 2, "color": color, "space": 0})

def set_all_cell_borders(table, visible) :
    color = "000000" if visible else "FFFFFF"
    for row in table.rows:
        for cell in row.cells:
            set_cell_border(
                cell,
                top={"val": "single", "sz": 0, "color": color},
                bottom={"val": "single", "sz": 0, "color": color},
                start={"val": "single", "sz": 0, "color": color},
                end={"val": "single", "sz": 0, "color": color}
            )

def create_table(doc, t):
    table = doc.add_table(rows=len(t), cols=len(t[0]))
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    table.allow_autofit = False
    table.style = 'Table Grid'
    for i in range(len(t)):
        row = table.rows[i]
        for j in range(len(t[i])):
            row.cells[j].text = str(t[i][j])
    set_all_cell_borders(table, False)
    tbl_pr = table._element.xpath('.//w:tblPr')[0]
    tbl_ind = OxmlElement('w:tblInd')
    tbl_ind.set(qn('w:w'), str(int(600)))
    tbl_ind.set(qn('w:type'), 'dxa')
    tbl_pr.append(tbl_ind)
    return table


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
    add_section_title(doc, "1. MOLECULE")
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
    table.columns[0].width = Pt(160);
    table.columns[1].width = Pt(320);
    display_vertical_lines(table, False)
    doc.add_paragraph()


    ### SECTION 2
    add_section_title(doc, "2. COMPUTATIONAL DETAILS")
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
    table = create_table(doc, t)
    set_all_cell_borders(table, False)
    display_vertical_lines(table)
    set_vertical_line(table, 1, False)
    doc.add_paragraph("\nJob type: Geometry optimization")
    table.columns[0].width = Pt(200)
    table.columns[1].width = Pt(200)
    table.columns[2].width = Pt(80)


    ### section 3 : results
    t = []
    add_section_title(doc, "3. RESULTS")
    # Common results / wavefunction :
    t.append(['Total molecular energy', "%.5f hartrees" %
                       data_ref["results"]["wavefunction"]["total_molecular_energy"], " "])
    homo_ind = data_ref["results"]["wavefunction"]["homo_indexes"]
    MO_energies = data_ref["results"]["wavefunction"]["MO_energies"]
    if len(homo_ind) == 2:
        # Unrestricted calculation: two columns of MO energies
        t.append(['Unrestricted calculation', 'Alpha spin MO',
                           'Beta spin MO'])  # indices begin at 0, remove brackets
        t.append(['HOMO number', homo_ind[0] + 1, homo_ind[1] + 1])
        t.append(['LUMO+1 energies', "%.2f eV" % MO_energies[0][homo_ind[0] + 2],
                           "%.2f eV" % MO_energies[1][homo_ind[1] + 2]])
        t.append(['LUMO   energies', "%.2f eV" % MO_energies[0][homo_ind[0] + 1],
                           "%.2f eV" % MO_energies[1][homo_ind[1] + 1]])
        t.append(['HOMO   energies', "%.2f eV" % MO_energies[0][homo_ind[0]],
                           "%.2f eV" % MO_energies[1][homo_ind[1]]])
        t.append(['HOMO-1 energies', "%.2f eV" % MO_energies[0][homo_ind[0] - 1],
                           "%.2f eV" % MO_energies[1][homo_ind[1] - 1]])
    else:
        t.append(['HOMO number', homo_ind[0] + 1, " "])
        t.append(['LUMO+1 energies', "%.2f eV" % MO_energies[0][homo_ind[0] + 2], " "])
        t.append(['LUMO   energies', "%.2f eV" % MO_energies[0][homo_ind[0] + 1], " "])
        t.append(['HOMO   energies', "%.2f eV" % MO_energies[0][homo_ind[0]], " "])
        t.append(['HOMO-1 energies', "%.2f eV" % MO_energies[0][homo_ind[0] - 1], " "])

        # CDFT Indices  table only in full report
    if report_type == 'full':
        t.append([" ", " ", " "])
        try:
            t.append(['CDFT indices: Electron Affinity', "%.4f hartrees" % data_ref["results"]["wavefunction"]["A"],""])
        except KeyError:
            pass
        try:
            t.append(['CDFT indices: Ionisation Potential', "%.4f hartrees" % data_ref["results"]["wavefunction"]["I"], ""])
        except KeyError:
            pass
        try:
            t.append(['CDFT indices: Electronegativity', "%.4f hartrees" % data_ref["results"]["wavefunction"]["Khi"], ""])
        except KeyError:
            pass
        try:
            t.append(['CDFT indices: Hardness', "%.4f hartrees" % data_ref["results"]["wavefunction"]["Eta"], ""])
        except KeyError:
            pass
        try:
            t.append(['CDFT indices: Electrophilicity', "%.4f " % data_ref["results"]["wavefunction"]["Omega"], ""])
        except KeyError:
            pass
        try:
            t.append(['CDFT indices: Electron-flow', "%.4f e-" % data_ref["results"]["wavefunction"]["DeltaN"], ""])
        except KeyError:
            pass
            # Specific calculations results:
            OPT_res_print = False
            for i, jsonfile in enumerate(json_list):
                # OPT calculation results:
                if ((job_types[i] == ['OPT']) or (job_types[i] == ['FREQ', 'OPT']) \
                    or job_types[i] == ['FREQ', 'OPT', 'TD']) and (OPT_res_print == False):
                    j = str(i + 1)
                    OPT_res_print = True  # to prevent repetition from OPT and FREQ
                    t.append([" ", " ", " "])
                    t.append(["Geometry optimization specific results", " ", " "])
                    t.append(['Converged nuclear repulsion energy',
                                       "%.5f Hartrees" % json_list[i]["results"]["geometry"][
                                           "nuclear_repulsion_energy_from_xyz"], " "])

                # FREQ calculation results:
                if job_types[i] == ['FREQ'] or job_types[i] == ['FREQ', 'OPT'] or job_types[i] == ['FREQ', 'OPT', 'TD']:
                    k = 0
                    j = str(k + 1)
                    t.append([" ", " ", " "])
                    t.append(["Frequency and Thermochemistry specific results", " ", " "])
                    try:
                        rtemper = json_list[i]["comp_details"]["freq"]["temperature"]
                    except KeyError:
                        rtemper = []
                    # ND-arrays
                    try:
                        vibrational_int = np.array(json_list[i]["results"]["freq"]["vibrational_int"])
                    except KeyError:
                        vibrational_int = []
                    try:
                        vibrational_freq = np.array(json_list[i]["results"]["freq"]["vibrational_freq"])
                    except KeyError:
                        vibrational_freq = []

                    if len(vibrational_int) == 0:
                        vibrational_int = []
                    else:
                        # Print number of negative frequencies
                        nb_negatives = np.sum(vibrational_freq < 0, axis=0)

                    if (len(vibrational_int) != 0) and (rtemper != "N/A"):
                        if "zero_point_energy" in json_list[i]["results"]["freq"]:
                            t.append(['Sum of electronic and zero-point energy',
                                               "%.5f Hartrees" % json_list[i]["results"]["freq"]["zero_point_energy"],
                                               " "])
                        if "electronic_thermal_energy" in json_list[i]["results"]["freq"]:
                            t.append(["Sum of electronic and thermal energies at  %.2f K" % rtemper,
                                               "%.5f Hartrees" % json_list[i]["results"]["freq"][
                                                   "electronic_thermal_energy"], " "])
                        if "enthalpy" in json_list[i]["results"]["freq"]:
                            t.append(["Enthalpy at %.2f K" % rtemper,
                                               "%.5f Hartrees" % json_list[i]["results"]["freq"]["enthalpy"], " "])
                        if "free_energy" in json_list[i]["results"]["freq"]:
                            t.append(["Gibbs free energy at %.2f K" % rtemper,
                                               "%.5f Hartrees" % json_list[i]["results"]["freq"]["free_energy"], " "])
                        if "entropy" in json_list[i]["results"]["freq"]:
                            t.append(["Entropy at %.2f K" % rtemper,
                                               "%.5f Hartrees" % json_list[i]["results"]["freq"]["entropy"], " "])
            # End of the big common result table.

            ## List of tables that are not job associated but dependent of data_ref.
            # Population analysis tables and Fukui condensed values table only in full reports
        if report_type == 'full':
            # Mulliken partial charges table
            try:
                mulliken = data_ref["results"]["wavefunction"]["Mulliken_partial_charges"]
            except KeyError:
                mulliken = []
            # test other population analysis
            try:
                hirsh = data_ref["results"]["wavefunction"]["Hirshfeld_partial_charges"]
            except KeyError:
                hirsh = []
            try:
                cm5 = data_ref["results"]["wavefunction"]["CM5_partial_charges"]
            except KeyError:
                cm5 = []


    table = create_table(doc, t)
    set_all_cell_borders(table, False)
    display_vertical_lines(table)
    set_vertical_line(table, 1, False)
    doc.add_paragraph("\nJob type: Geometry optimization")
    table.columns[0].width = Pt(200)
    table.columns[1].width = Pt(200)
    table.columns[2].width = Pt(80)

    doc.save("test.docx")
