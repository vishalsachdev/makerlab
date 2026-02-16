#!/usr/bin/env python3
"""Generate summer camp form PDFs for Illinois MakerLab.

Based on CU Community Fab Lab forms, adapted with MakerLab branding and contact info.
Generates 4 individual forms + 1 combined packet.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.colors import HexColor, black, white

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'summer', 'forms')

ILLINOIS_ORANGE = HexColor('#FF5F05')
ILLINOIS_BLUE = HexColor('#13294B')

ORG_NAME = 'Illinois MakerLab'
ORG_ADDRESS = '515 East Gregory Drive, BIF Room 3030'
ORG_CITY = 'Champaign, IL 61820'
ORG_EMAIL = 'uimakerlab@illinois.edu'
ORG_WEBSITE = 'makerlab.illinois.edu'
DIRECTOR_NAME = 'Dr. Vishal Sachdev'
DIRECTOR_TITLE = 'Director, Illinois MakerLab'
DIRECTOR_DEPT = 'Gies College of Business'
DIRECTOR_UNIV = 'University of Illinois at Urbana-Champaign'


def get_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        'FormTitle', parent=styles['Title'],
        fontSize=16, textColor=ILLINOIS_BLUE, spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        'FormSubtitle', parent=styles['Normal'],
        fontSize=10, textColor=ILLINOIS_BLUE, alignment=TA_CENTER, spaceAfter=12
    ))
    styles.add(ParagraphStyle(
        'SectionHeader', parent=styles['Heading2'],
        fontSize=12, textColor=ILLINOIS_BLUE, spaceBefore=16, spaceAfter=6,
        borderWidth=0, borderPadding=0
    ))
    styles.add(ParagraphStyle(
        'FormBody', parent=styles['Normal'],
        fontSize=10, leading=14, spaceAfter=4, alignment=TA_LEFT
    ))
    styles.add(ParagraphStyle(
        'FormBodyJustify', parent=styles['Normal'],
        fontSize=10, leading=14, spaceAfter=4, alignment=TA_JUSTIFY
    ))
    styles.add(ParagraphStyle(
        'FormSmall', parent=styles['Normal'],
        fontSize=8, leading=10, spaceAfter=2
    ))
    styles.add(ParagraphStyle(
        'SignLine', parent=styles['Normal'],
        fontSize=10, leading=14, spaceBefore=20, spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        'FieldLine', parent=styles['Normal'],
        fontSize=10, leading=20, spaceAfter=2
    ))
    return styles


def blank_line(width='100%'):
    return HRFlowable(width=width, thickness=0.5, color=black, spaceAfter=4, spaceBefore=2)


def field_row(label, width='100%'):
    return Paragraph(f'<b>{label}:</b> ___________________________________________________________________________', get_styles()['FieldLine'])


def signature_block():
    styles = get_styles()
    elements = []
    elements.append(Spacer(1, 20))

    sig_data = [
        ['_' * 50, '', '_' * 25],
        ['Signature of Parent/Guardian of Minor (under 18)', '', 'Date'],
    ]
    sig_table = Table(sig_data, colWidths=[3.5 * inch, 0.5 * inch, 2.5 * inch])
    sig_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ]))
    elements.append(sig_table)
    return elements


def header_block(styles):
    elements = []
    elements.append(Paragraph(f'<b>{ORG_NAME}</b>', styles['FormTitle']))
    elements.append(Paragraph(
        f'{ORG_ADDRESS} | {ORG_CITY}<br/>'
        f'Email: {ORG_EMAIL} | Web: {ORG_WEBSITE}',
        styles['FormSubtitle']
    ))
    elements.append(HRFlowable(width='100%', thickness=2, color=ILLINOIS_BLUE, spaceAfter=12))
    return elements


def build_emergency_form(filename):
    styles = get_styles()
    doc = SimpleDocTemplate(
        filename, pagesize=letter,
        leftMargin=0.75 * inch, rightMargin=0.75 * inch,
        topMargin=0.6 * inch, bottomMargin=0.6 * inch
    )
    elements = []

    elements.extend(header_block(styles))
    elements.append(Paragraph('EMERGENCY CONTACT AND MEDICAL INFORMATION', styles['FormTitle']))
    elements.append(Paragraph(
        'Only one form needs to be submitted per camper if registering for multiple camps. '
        'Please complete and return this form by one of the following methods:',
        styles['FormBody']
    ))

    method_data = [
        [Paragraph('<b>Email:</b>', styles['FormBody']),
         Paragraph('<b>Mail:</b>', styles['FormBody']),
         Paragraph('<b>In Person:</b>', styles['FormBody'])],
        [Paragraph(ORG_EMAIL, styles['FormBody']),
         Paragraph(f'{ORG_NAME}<br/>{ORG_ADDRESS}<br/>{ORG_CITY}', styles['FormBody']),
         Paragraph('Bring it with you the<br/>first day of camp', styles['FormBody'])],
    ]
    method_table = Table(method_data, colWidths=[2.3 * inch, 2.3 * inch, 2.3 * inch])
    method_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(method_table)
    elements.append(Spacer(1, 8))

    # Camper Information
    elements.append(Paragraph('CAMPER INFORMATION', styles['SectionHeader']))
    elements.append(field_row('NAME'))
    elements.append(Paragraph(
        '<b>ADDRESS:</b> _________________________________________________________________________<br/>'
        '<font size="8">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
        'Number / Street&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
        'City&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
        'State&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Zip Code</font>',
        styles['FieldLine']
    ))
    elements.append(Paragraph(
        '<b>AGE:</b> ____________ <b>GENDER:</b> ____________ <b>DATE OF BIRTH:</b> _____/_____/_________',
        styles['FieldLine']
    ))

    # Parent/Guardian
    elements.append(Paragraph('PARENT / GUARDIAN / OTHER', styles['SectionHeader']))
    elements.append(field_row('NAME'))
    elements.append(Paragraph(
        '<b>RELATIONSHIP:</b> ____________________________________________________________________',
        styles['FieldLine']
    ))
    elements.append(Paragraph(
        '<b>ADDRESS:</b> _________________________________________________________________________<br/>'
        '<font size="8">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
        'Number / Street&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
        'City&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
        'State&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Zip Code</font>',
        styles['FieldLine']
    ))
    elements.append(Paragraph(
        '<b>EMAIL:</b> ___________________________________________________________________________',
        styles['FieldLine']
    ))

    # Emergency Contact
    elements.append(Paragraph('EMERGENCY CONTACT', styles['SectionHeader']))
    elements.append(field_row('NAME'))
    elements.append(Paragraph(
        '<b>RELATIONSHIP:</b> ____________________________________________________________________',
        styles['FieldLine']
    ))
    elements.append(Paragraph(
        '<b>ADDRESS:</b> _________________________________________________________________________<br/>'
        '<font size="8">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
        'Number / Street&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
        'City&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
        'State&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Zip Code</font>',
        styles['FieldLine']
    ))
    elements.append(Paragraph(
        '<b>EMAIL:</b> ___________________________________________________________________________',
        styles['FieldLine']
    ))

    # Health Information
    elements.append(Paragraph('HEALTH INFORMATION STATEMENT', styles['SectionHeader']))
    elements.append(Paragraph(
        'Check below and provide any information you feel the staff may need to maximize the safety and the '
        'well-being of the attendee. In case of emergency, this health information may be the only source of '
        'accurate important information. This information is confidential.',
        styles['FormBodyJustify']
    ))
    conditions = [
        'Nervous or Mental (epilepsy, emotional stress, convulsion)',
        'Lung Disease (asthma, persistent cough, tuberculosis)',
        'Hay Fever or Allergies',
        'Allergy to Medicines (including penicillin, tetanus)',
        'Impaired Sight or Hearing, Chronic Ear Infections',
        'Recent Surgical Operations, Accidents or Injuries',
        'Diabetes, Heart Disease, or Blood Disorder',
        'Other Medical Conditions',
    ]
    for cond in conditions:
        elements.append(Paragraph(
            f'[ ] {cond} ___________________________________________',
            styles['FormBody']
        ))

    elements.append(Spacer(1, 8))
    elements.append(Paragraph(
        '<b>Current Medications:</b> _______________________________________________________________',
        styles['FieldLine']
    ))
    elements.append(Paragraph(
        '<b>Family Physician:</b> ____________________________ <b>Email:</b> ____________________________',
        styles['FieldLine']
    ))

    elements.extend(signature_block())
    doc.build(elements)
    print(f'  Created: {filename}')


def build_waiver(filename):
    styles = get_styles()
    doc = SimpleDocTemplate(
        filename, pagesize=letter,
        leftMargin=0.75 * inch, rightMargin=0.75 * inch,
        topMargin=0.6 * inch, bottomMargin=0.6 * inch
    )
    elements = []

    elements.extend(header_block(styles))

    elements.append(Paragraph(
        '<b>Name of Participant:</b> _______________________________________________________________',
        styles['FieldLine']
    ))
    elements.append(Spacer(1, 8))

    elements.append(Paragraph(
        'WAIVER OF LIABILITY, ASSUMPTION OF RISK, AND INDEMNITY AGREEMENT',
        styles['FormTitle']
    ))

    elements.append(Paragraph('WAIVER', styles['SectionHeader']))
    elements.append(Paragraph(
        f'In consideration of being permitted to participate in any way in {ORG_NAME} Programs '
        f'taking place at the {ORG_NAME} at the University of Illinois campus, I, for myself, my heirs, '
        'personal representatives or assigns, do hereby release, waive, discharge, and covenant not to sue '
        'the Board of Trustees of the University of Illinois and its respective officers, employees, and '
        'agents from liability from any and all claims including those which result in personal injury, '
        f'accidents or illnesses (including death), and property loss arising from, but not limited to, '
        f'participation in {ORG_NAME} Programs.',
        styles['FormBodyJustify']
    ))

    elements.append(Paragraph('ASSUMPTION OF RISKS', styles['SectionHeader']))
    elements.append(Paragraph(
        f'The {ORG_NAME} has several safety guidelines for using equipment in the lab, which if '
        'followed, result in safe enjoyment of the facilities. However, participation in fabrication and '
        'making workshops carries with it certain inherent risks that cannot be completely eliminated '
        'regardless of the care taken to avoid injuries. The specific risks vary from one activity to '
        'another, but the risks range from 1) minor injuries such as small cuts, scratches, or burns, to '
        '2) major injuries such as eye injury or loss of sight, cuts, and burns. I have read the previous '
        'paragraphs and I know, understand, and appreciate these and other risks that are inherent in use '
        f'of the {ORG_NAME}. I hereby assert that my participation is voluntary and that I knowingly '
        'assume all such risks.',
        styles['FormBodyJustify']
    ))

    elements.append(Paragraph('INDEMNIFICATION AND HOLD HARMLESS', styles['SectionHeader']))
    elements.append(Paragraph(
        'I also agree to INDEMNIFY AND HOLD the Board of Trustees of the University of Illinois HARMLESS '
        'from any and all claims, actions, suits, procedures, costs, expenses, damages and liabilities, '
        'including attorney\'s fees, brought as a result of my involvement in '
        f'{ORG_NAME} Programs and to reimburse it for any such expenses incurred.',
        styles['FormBodyJustify']
    ))

    elements.append(Paragraph('ACKNOWLEDGEMENT OF UNDERSTANDING', styles['SectionHeader']))
    elements.append(Paragraph(
        'I have read this waiver of liability, assumption of risk, and indemnity agreement, fully and '
        'understand its terms, and understand that I am giving up substantial rights, including my right '
        'to sue. I acknowledge that I am signing the agreement freely and voluntarily and intend by my '
        'signature to be a complete and unconditional release of all liability to the greatest extent '
        'allowed by law.',
        styles['FormBodyJustify']
    ))

    elements.extend(signature_block())
    doc.build(elements)
    print(f'  Created: {filename}')


def build_photo_waiver_minors(filename):
    styles = get_styles()
    doc = SimpleDocTemplate(
        filename, pagesize=letter,
        leftMargin=0.75 * inch, rightMargin=0.75 * inch,
        topMargin=0.75 * inch, bottomMargin=0.75 * inch
    )
    elements = []

    elements.extend(header_block(styles))
    elements.append(Paragraph('VIDEO / PHOTOGRAPH RELEASE — MINORS', styles['FormTitle']))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(
        'I, _______________________________________________, the parent or legal guardian of '
        '________________________________________________, hereby give consent for my child\'s',
        styles['FormBody']
    ))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(
        '&nbsp;&nbsp;&nbsp;&nbsp;&#9744; photograph &nbsp;&nbsp;&nbsp;&nbsp;(please check each box for which you give consent)',
        styles['FormBody']
    ))
    elements.append(Paragraph(
        '&nbsp;&nbsp;&nbsp;&nbsp;&#9744; video',
        styles['FormBody']
    ))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(
        f'to be recorded in the course of participating in ____________________________ at the '
        f'{ORG_NAME}, under the general supervision and direction of {DIRECTOR_NAME}. I understand that these '
        'photographs or video footage may be used for illustrative or informational purposes on the '
        f'organization\'s website ({ORG_WEBSITE}), Instagram (instagram.com/uimakerlab/), '
        'Facebook (facebook.com/uimakerlab/), or in publications. '
        'I understand that my child will not be identified by name. I understand that I can contact '
        f'the MakerLab at any time at the address and/or email given below if I have any questions.',
        styles['FormBodyJustify']
    ))

    # Signature lines
    elements.append(Spacer(1, 24))
    sig_data = [
        ['_' * 50, '', '_' * 25],
        ['Signature of Parent/Guardian', '', 'Date'],
        ['', '', ''],
        ['_' * 50, '', '_' * 25],
        ['Signature of Child Participant', '', 'Date'],
        ['', '', ''],
        ['_' * 50, '', '_' * 25],
        [f'Signature of {ORG_NAME} Representative', '', 'Date'],
    ]
    sig_table = Table(sig_data, colWidths=[3.5 * inch, 0.5 * inch, 2.5 * inch])
    sig_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    elements.append(sig_table)

    # Director info
    elements.append(Spacer(1, 24))
    elements.append(HRFlowable(width='40%', thickness=0.5, color=ILLINOIS_BLUE, spaceAfter=8))
    elements.append(Paragraph(f'<b>{DIRECTOR_NAME}</b>', styles['FormBody']))
    elements.append(Paragraph(DIRECTOR_TITLE, styles['FormBody']))
    elements.append(Paragraph(DIRECTOR_DEPT, styles['FormBody']))
    elements.append(Paragraph(DIRECTOR_UNIV, styles['FormBody']))
    elements.append(Paragraph(f'Email: {ORG_EMAIL}', styles['FormBody']))

    doc.build(elements)
    print(f'  Created: {filename}')


def build_photo_waiver_adults(filename):
    styles = get_styles()
    doc = SimpleDocTemplate(
        filename, pagesize=letter,
        leftMargin=0.75 * inch, rightMargin=0.75 * inch,
        topMargin=0.75 * inch, bottomMargin=0.75 * inch
    )
    elements = []

    elements.extend(header_block(styles))
    elements.append(Paragraph('VIDEO / PHOTOGRAPH RELEASE — ADULTS', styles['FormTitle']))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(
        'I, _______________________________________________, hereby give consent for my',
        styles['FormBody']
    ))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(
        '&nbsp;&nbsp;&nbsp;&nbsp;&#9744; photograph &nbsp;&nbsp;&nbsp;&nbsp;(please check each box for which you give consent)',
        styles['FormBody']
    ))
    elements.append(Paragraph(
        '&nbsp;&nbsp;&nbsp;&nbsp;&#9744; video',
        styles['FormBody']
    ))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(
        f'to be recorded in the course of participating in ____________________________ at the '
        f'{ORG_NAME}, under the general supervision and direction of {DIRECTOR_NAME}. I understand that these '
        'photographs or video footage may be used for illustrative or informational purposes on the '
        f'organization\'s website ({ORG_WEBSITE}), Instagram (instagram.com/uimakerlab/), '
        'Facebook (facebook.com/uimakerlab/), or in publications. '
        f'I understand that I can contact the MakerLab at any time at the address and/or email given '
        'below if I have any questions.',
        styles['FormBodyJustify']
    ))

    # Signature lines
    elements.append(Spacer(1, 24))
    sig_data = [
        ['_' * 50, '', '_' * 25],
        ['Signature of Participant', '', 'Date'],
        ['', '', ''],
        ['_' * 50, '', '_' * 25],
        [f'Signature of {ORG_NAME} Representative', '', 'Date'],
    ]
    sig_table = Table(sig_data, colWidths=[3.5 * inch, 0.5 * inch, 2.5 * inch])
    sig_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    elements.append(sig_table)

    # Director info
    elements.append(Spacer(1, 24))
    elements.append(HRFlowable(width='40%', thickness=0.5, color=ILLINOIS_BLUE, spaceAfter=8))
    elements.append(Paragraph(f'<b>{DIRECTOR_NAME}</b>', styles['FormBody']))
    elements.append(Paragraph(DIRECTOR_TITLE, styles['FormBody']))
    elements.append(Paragraph(DIRECTOR_DEPT, styles['FormBody']))
    elements.append(Paragraph(DIRECTOR_UNIV, styles['FormBody']))
    elements.append(Paragraph(f'Email: {ORG_EMAIL}', styles['FormBody']))

    doc.build(elements)
    print(f'  Created: {filename}')


def build_combined_packet(filename, individual_files):
    """Build a combined PDF packet from individual form PDFs."""
    # We'll just build a fresh combined doc with all forms inline
    styles = get_styles()
    doc = SimpleDocTemplate(
        filename, pagesize=letter,
        leftMargin=0.75 * inch, rightMargin=0.75 * inch,
        topMargin=0.6 * inch, bottomMargin=0.6 * inch
    )

    # For the combined packet, we import and merge PDFs
    # Since reportlab can't merge existing PDFs easily, we'll use PyPDF2 or just
    # regenerate. Let's use PyPDF2 to merge.
    try:
        from PyPDF2 import PdfMerger
        merger = PdfMerger()
        for f in individual_files:
            merger.append(f)
        merger.write(filename)
        merger.close()
        print(f'  Created: {filename} (merged from individual forms)')
    except ImportError:
        # Fallback: just create a cover page noting individual forms
        elements = []
        elements.extend(header_block(styles))
        elements.append(Paragraph('SUMMER CAMP FORM PACKET', styles['FormTitle']))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(
            'This packet includes the following forms. Please complete all required forms '
            'and return them before the first day of camp.',
            styles['FormBody']
        ))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph('<b>Required Forms:</b>', styles['FormBody']))
        elements.append(Paragraph('1. Emergency Contact &amp; Medical Information Form', styles['FormBody']))
        elements.append(Paragraph('2. Waiver of Liability, Assumption of Risk, and Indemnity Agreement', styles['FormBody']))
        elements.append(Spacer(1, 8))
        elements.append(Paragraph('<b>Optional Forms:</b>', styles['FormBody']))
        elements.append(Paragraph('3. Photo/Video Release Form — Minors', styles['FormBody']))
        elements.append(Paragraph('4. Photo/Video Release Form — Adults', styles['FormBody']))
        elements.append(Spacer(1, 16))
        elements.append(Paragraph(
            'Individual forms are also available for download on our website.',
            styles['FormBody']
        ))
        doc.build(elements)
        print(f'  Created: {filename} (cover page only - install PyPDF2 for merged version)')


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    emergency = os.path.join(OUTPUT_DIR, 'Emergency-Medical-Contact-Form.pdf')
    waiver = os.path.join(OUTPUT_DIR, 'Waiver-of-Liability.pdf')
    photo_minors = os.path.join(OUTPUT_DIR, 'Photo-Waiver-Minors.pdf')
    photo_adults = os.path.join(OUTPUT_DIR, 'Photo-Waiver-Adults.pdf')
    combined = os.path.join(OUTPUT_DIR, 'Summer-Camp-Forms.pdf')

    print('Generating Illinois MakerLab camp forms...')
    build_emergency_form(emergency)
    build_waiver(waiver)
    build_photo_waiver_minors(photo_minors)
    build_photo_waiver_adults(photo_adults)
    build_combined_packet(combined, [emergency, waiver, photo_minors, photo_adults])
    print('Done!')


if __name__ == '__main__':
    main()
