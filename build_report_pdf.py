"""
build_report_pdf.py
Generates the publication-quality ECSCI24302 Machine Learning Essentials Project Report in .pdf format.
Uses ReportLab to ensure pixel-perfect academic typesetting, running headers, footers, tables, and embedded figures.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            # Suppress header and footer on cover page
            return

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Header
        self.drawString(54, 11 * inch - 36, "ECSCI24302 – Machine Learning Essentials  |  Project-Based Learning Report")
        self.drawRightString(8.5 * inch - 54, 11 * inch - 36, "Adani University")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)

        # Footer
        self.line(54, 46, 8.5 * inch - 54, 46)
        self.drawString(54, 34, "Indian Railways Train Delay Prediction & Network Punctuality Analytics")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 54, 34, page_str)
        self.restoreState()

def build_pdf(output_path="deliverables/Project_Report.pdf"):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Colors
    c_navy = colors.HexColor("#0B2545")
    c_slate = colors.HexColor("#1E4976")
    c_blue = colors.HexColor("#2563EB")
    c_charcoal = colors.HexColor("#1E293B")
    c_gray = colors.HexColor("#64748B")
    c_light = colors.HexColor("#F8FAFC")

    # Typography styles
    styles.add(ParagraphStyle('DocTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=22, leading=26, textColor=c_navy, alignment=1))
    styles.add(ParagraphStyle('DocSub', parent=styles['Normal'], fontName='Helvetica', fontSize=11, leading=15, textColor=c_charcoal, alignment=1))
    styles.add(ParagraphStyle('UniHeader', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=15, leading=18, textColor=c_navy, alignment=1))
    styles.add(ParagraphStyle('DeptHeader', parent=styles['Normal'], fontName='Helvetica', fontSize=10.5, leading=14, textColor=c_slate, alignment=1))
    styles.add(ParagraphStyle('CourseHeader', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=c_blue, alignment=1))
    
    styles.add(ParagraphStyle('Heading1Custom', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=15, leading=19, textColor=c_navy, spaceBefore=16, spaceAfter=6, keepWithNext=True))
    styles.add(ParagraphStyle('Heading2Custom', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=c_slate, spaceBefore=12, spaceAfter=4, keepWithNext=True))
    styles.add(ParagraphStyle('Heading3Custom', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10.5, leading=14, textColor=c_blue, spaceBefore=8, spaceAfter=2, keepWithNext=True))

    styles.add(ParagraphStyle('BodyCustom', parent=styles['Normal'], fontName='Helvetica', fontSize=9.5, leading=13.5, textColor=c_charcoal, spaceBefore=0, spaceAfter=5))
    styles.add(ParagraphStyle('BulletCustom', parent=styles['Normal'], fontName='Helvetica', fontSize=9.5, leading=13.5, textColor=c_charcoal, leftIndent=15, firstLineIndent=-10, spaceBefore=1, spaceAfter=2))
    styles.add(ParagraphStyle('CaptionCustom', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=8.5, leading=11, textColor=c_gray, alignment=1, spaceBefore=3, spaceAfter=8))
    styles.add(ParagraphStyle('TableCell', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=11, textColor=c_charcoal))
    styles.add(ParagraphStyle('TableHead', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=colors.white))
    styles.add(ParagraphStyle('CalloutTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9.5, leading=12, textColor=c_blue))
    styles.add(ParagraphStyle('CalloutBody', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=12, textColor=c_charcoal))

    story = []

    # -------------------------------------------------------------
    # TITLE PAGE
    # -------------------------------------------------------------
    story.append(Spacer(1, 20))
    story.append(Paragraph("ADANI UNIVERSITY", styles['UniHeader']))
    story.append(Paragraph("Faculty of Engineering and Technology<br/>Department of Computer Science & Engineering", styles['DeptHeader']))
    story.append(Spacer(1, 14))
    story.append(Paragraph("ECSCI24302 – MACHINE LEARNING ESSENTIALS<br/>PROJECT-BASED LEARNING (PBL) FINAL REPORT", styles['CourseHeader']))
    story.append(Spacer(1, 16))
    story.append(Paragraph("Indian Railways Train Delay Prediction &<br/>Network Punctuality Analytics", styles['DocTitle']))
    story.append(Spacer(1, 8))
    story.append(Paragraph("An End-to-End Supervised Machine Learning Workflow from Exploratory Analysis to Decision-Support Deployment", styles['DocSub']))
    story.append(Spacer(1, 25))

    # Student Team Box
    team_data = [
        [Paragraph("Role", styles['TableHead']), Paragraph("Student Full Name", styles['TableHead']), Paragraph("Enrollment Number", styles['TableHead'])],
        [Paragraph("Team Lead", styles['TableCell']), Paragraph("[Student Name 1 - To Be Filled]", styles['TableCell']), Paragraph("[Enrollment No. 1 - To Be Filled]", styles['TableCell'])],
        [Paragraph("Team Member 2", styles['TableCell']), Paragraph("[Student Name 2 - To Be Filled]", styles['TableCell']), Paragraph("[Enrollment No. 2 - To Be Filled]", styles['TableCell'])],
        [Paragraph("Team Member 3", styles['TableCell']), Paragraph("[Student Name 3 - To Be Filled]", styles['TableCell']), Paragraph("[Enrollment No. 3 - To Be Filled]", styles['TableCell'])],
        [Paragraph("Faculty Guide", styles['TableCell']), Paragraph("[Faculty Mentor Name - To Be Filled]", styles['TableCell']), Paragraph("[Department / Designation]", styles['TableCell'])]
    ]
    t_team = Table(team_data, colWidths=[1.5*inch, 3.2*inch, 2.3*inch])
    t_team.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [c_light, colors.white]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1"))
    ]))
    story.append(t_team)
    story.append(Spacer(1, 40))

    meta_text = "Academic Year: 2026–2027   |   Submission Date: November 2026   |   Location: Ahmedabad, India"
    story.append(Paragraph(meta_text, ParagraphStyle('Meta', parent=styles['Normal'], fontName='Helvetica', fontSize=9, textColor=c_gray, alignment=1)))
    story.append(PageBreak())

    # Helper for Callouts
    def make_callout(title, body):
        content = [
            [Paragraph(f"ENGINEERING INSIGHT: {title}", styles['CalloutTitle'])],
            [Paragraph(body, styles['CalloutBody'])]
        ]
        t = Table(content, colWidths=[7.0*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
            ('LINELEFT', (0,0), (0,-1), 3.0, c_blue),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ]))
        return t

    # Helper for Images
    def make_img(path, caption, w=6.4*inch, h=2.5*inch):
        flowables = []
        if os.path.exists(path):
            flowables.append(Image(path, width=w, height=h))
            flowables.append(Paragraph(caption, styles['CaptionCustom']))
        return flowables

    # -------------------------------------------------------------
    # ABSTRACT / PROJECT SUMMARY
    # -------------------------------------------------------------
    story.append(Paragraph("Abstract / Project Summary", styles['Heading1Custom']))
    story.append(Paragraph(
        "Indian Railways operates the world's fourth-largest railway network, running over 13,000 passenger trains "
        "daily across 68,000 route kilometers. Ensuring schedule punctuality is vital for passenger satisfaction, economic "
        "productivity, and network resource management. Train delays arise from an intricate web of interacting factors, "
        "including network congestion, weather disruptions (such as winter fog and monsoons), infrastructure bottlenecks, "
        "locomotive/coach maintenance age, and knock-on propagation from late incoming rakes.", styles['BodyCustom']))
    story.append(Paragraph(
        "This project delivers an end-to-end Machine Learning pipeline to predict train delay outcomes (>15 minutes arrival delay at destination), "
        "strictly following the 19-stage Problem-Based Learning (PBL) curriculum outlined in the course guidelines (ECSCI24302). "
        "The problem is framed as a supervised binary classification task. The workflow encompasses: rigorous data quality audits, "
        "strict data leakage prevention (quarantining post-event delay metrics), the creation of 11 domain-specific engineered features, "
        "NumPy-based Interquartile Range (IQR) outlier capping, stratified 80:20 train-validation splitting, Scikit-learn/Pandas pipeline serialization, "
        "systematic hyperparameter tuning using cross-validation, comprehensive multi-metric model evaluation, granular error analysis across railway zones, "
        "and model interpretability using feature importances.", styles['BodyCustom']))
    story.append(Paragraph(
        "To satisfy computational constraints while maintaining experimental rigor, model development and tuning were conducted on a curated, "
        "representative sample of 10,000 training records (8,000 training partition, 2,000 validation partition). Seven model configurations were evaluated: "
        "a Dummy Classifier baseline, Logistic Regression, Decision Tree, Random Forest, LightGBM, and hyperparameter-tuned variants of Random Forest and LightGBM. "
        "Among all models, Tuned LightGBM emerged as the champion operational model, achieving an Accuracy of 85.85%, Recall of 92.10%, and an F1-Score of 0.9038. "
        "Logistic Regression demonstrated the highest discrimination capacity with a ROC-AUC of 0.9229. The pipeline was deployed in two production-grade artifacts: "
        "(1) a submission file predicting delay probabilities for all 375,000 unseen test journeys passing all structural integrity audits, and "
        "(2) an interactive Streamlit web application providing single-journey risk categorization (Green <40%, Amber 40–65%, Red >65%) and network punctuality analytics.", styles['BodyCustom']))
    story.append(Paragraph(
        "All reported metrics reflect the controlled 10,000-record experimental sample and are transparently presented without exaggeration. "
        "This report provides an academically sound, reproducible, and easily defensible technical foundation for viva voce examination.", styles['BodyCustom']))

    # -------------------------------------------------------------
    # 1. INTRODUCTION
    # -------------------------------------------------------------
    story.append(Paragraph("1. Introduction", styles['Heading1Custom']))
    story.append(Paragraph(
        "The Indian Railways (IR) network is an indispensable lifeline of India's transport infrastructure, carrying over 23 million "
        "passengers and 3 million tonnes of freight every single day. Operating a mixed-traffic railway system—where high-speed premier expresses "
        "(such as Vande Bharat and Rajdhani), slow passenger trains, and heavy freight trains share the same physical tracks—makes schedule management "
        "exceptionally difficult. A delay experienced by a single train at a busy junction cascades through the entire network, "
        "triggering secondary delays across multiple operational zones.", styles['BodyCustom']))
    story.append(Paragraph(
        "Machine Learning provides an analytical paradigm to discover non-linear patterns within historical operational data. By capturing the multi-factorial "
        "relationships between track congestion, seasonal weather severity, scheduled speed, stop density, equipment age, and incoming rake delays, predictive "
        "models can forecast delay probabilities well before a journey reaches its destination.", styles['BodyCustom']))
    
    story.append(Paragraph("1.1 Educational Journey: What We Did, Why We Did It, and What We Learned", styles['Heading2Custom']))
    story.append(Paragraph("• <b>What We Did:</b> We built a complete, reproducible Machine Learning pipeline using Python, NumPy, Pandas, Scikit-learn, and LightGBM, covering all 19 stages from raw data ingestion to interactive web deployment.", styles['BulletCustom']))
    story.append(Paragraph("• <b>Why We Did It:</b> Rather than treating Machine Learning as an isolated black-box API call, our goal was to understand the end-to-end data science lifecycle: how data quality flaws are diagnosed, how data leakage is prevented, how domain engineering creates predictive power, and how models are rigorously audited.", styles['BulletCustom']))
    story.append(Paragraph("• <b>What We Learned:</b> We learned that real-world Machine Learning success depends heavily on proper data hygiene and feature design. Simply throwing algorithms at raw data leads to leakage or trivial models. Furthermore, we discovered that evaluating imbalanced datasets with accuracy alone is dangerous; a trivial majority-class baseline achieves 72.15% accuracy while possessing zero predictive skill.", styles['BulletCustom']))

    # -------------------------------------------------------------
    # 2. PROBLEM STATEMENT AND MOTIVATION
    # -------------------------------------------------------------
    story.append(Paragraph("2. Problem Statement and Motivation", styles['Heading1Custom']))
    story.append(Paragraph("2.1 Problem Formulation", styles['Heading2Custom']))
    story.append(Paragraph(
        "The objective is to formulate and solve a supervised binary classification problem that predicts whether a scheduled train journey will arrive at its destination with a delay exceeding 15 minutes.", styles['BodyCustom']))
    story.append(Paragraph(
        "Mathematically, let <i>X</i> denote the feature vector of pre-departure operational and infrastructure attributes. The target variable is defined as:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>is_delayed = 1</b>, if destination arrival delay &gt; 15 minutes (Delayed)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>is_delayed = 0</b>, if destination arrival delay &le; 15 minutes (On-Time)", styles['BodyCustom']))
    
    story.append(Paragraph("2.2 Project Objectives", styles['Heading2Custom']))
    objectives = [
        ("Objective 1: ", "Acquire, inspect, and profile the Indian Railways dataset, identifying schema types, identifier columns, and data distributions."),
        ("Objective 2: ", "Conduct systematic data cleaning and exploratory data analysis (EDA) to expose class imbalance, seasonal patterns, and network bottlenecks."),
        ("Objective 3: ", "Enforce strict target leakage safeguards by quarantining post-event variables that would never be available at departure time."),
        ("Objective 4: ", "Formulate 11 domain-specific engineered features capturing scheduled travel speed, stop density, weather severity, equipment wear, and network vulnerability."),
        ("Objective 5: ", "Implement robust NumPy-based Interquartile Range (IQR) Winsorization to cap extreme outlier values without discarding records."),
        ("Objective 6: ", "Establish a benchmark baseline using a Dummy Classifier to prove the value added by trained machine learning models."),
        ("Objective 7: ", "Train and tune multiple supervised learning algorithms: Logistic Regression, Decision Tree, Random Forest, and LightGBM."),
        ("Objective 8: ", "Evaluate all models using a multi-metric framework: Accuracy, Precision, Recall, F1-Score, and ROC-AUC, supported by ROC curves and confusion matrices."),
        ("Objective 9: ", "Conduct granular error analysis across railway zones and train categories to understand where and why models misclassify journeys."),
        ("Objective 10: ", "Deploy the champion model into an interactive Streamlit decision-support application and generate verified predictions for 375,000 test journeys.")
    ]
    for pfx, desc in objectives:
        story.append(Paragraph(f"• <b>{pfx}</b>{desc}", styles['BulletCustom']))

    story.append(Paragraph("2.3 Real-World Relevance and Operational Positioning", styles['Heading2Custom']))
    story.append(Paragraph(
        "In a live railway control room, train controllers (dispatchers) must make split-second decisions regarding track allocation, precedence at junctions, "
        "and platform assignments. Providing controllers with an automated delay probability score hours in advance allows them to proactively reroute trains, "
        "adjust dwell times, or alert connecting stations. Crucially, this project is positioned as an analytical decision-support prototype—not an autonomous "
        "dispatch system. The model assists human decision-makers; it does not replace operational safety protocols.", styles['BodyCustom']))

    # -------------------------------------------------------------
    # 3. DATASET DESCRIPTION AND SOURCE
    # -------------------------------------------------------------
    story.append(Paragraph("3. Dataset Description and Source", styles['Heading1Custom']))
    story.append(Paragraph("3.1 Dataset Origin and File Structure", styles['Heading2Custom']))
    story.append(Paragraph(
        "The project utilizes the Indian Railways Train Delay Prediction dataset hosted on Kaggle. "
        "The repository maintains the input CSV files locally within the data/ directory (gitignored):", styles['BodyCustom']))
    
    file_tbl_data = [
        [Paragraph("File Name", styles['TableHead']), Paragraph("File Size", styles['TableHead']), Paragraph("Dimensions", styles['TableHead']), Paragraph("Operational Purpose", styles['TableHead'])],
        [Paragraph("ir_train.csv", styles['TableCell']), Paragraph("337 MB", styles['TableCell']), Paragraph("1,500,000 rows x 45 cols", styles['TableCell']), Paragraph("Supervised training dataset containing target is_delayed", styles['TableCell'])],
        [Paragraph("ir_test.csv", styles['TableCell']), Paragraph("76 MB", styles['TableCell']), Paragraph("375,000 rows x 42 cols", styles['TableCell']), Paragraph("Unlabeled evaluation set used for test-set inference", styles['TableCell'])],
        [Paragraph("ir_data_dictionary.csv", styles['TableCell']), Paragraph("4.2 KB", styles['TableCell']), Paragraph("45 rows x 3 cols", styles['TableCell']), Paragraph("Official metadata attribute definitions and descriptions", styles['TableCell'])],
        [Paragraph("ir_sample_submission.csv", styles['TableCell']), Paragraph("5.1 MB", styles['TableCell']), Paragraph("375,000 rows x 2 cols", styles['TableCell']), Paragraph("Submission schema template (journey_id, is_delayed)", styles['TableCell'])]
    ]
    t_files = Table(file_tbl_data, colWidths=[1.5*inch, 0.8*inch, 2.0*inch, 2.7*inch])
    t_files.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [c_light, colors.white]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_files)
    story.append(Spacer(1, 8))

    story.append(Paragraph("3.2 Experimental Sampling Rationale", styles['Heading2Custom']))
    story.append(make_callout(
        "Why 10,000 Records Were Sampled for Model Training",
        "While ir_train.csv contains 1.5 million rows, one-hot encoding across multiple categorical attributes (train types, railway zones, station categories) "
        "expands the feature space to over 8,100 columns. On standard student workstation hardware (16GB RAM), fitting full ensemble models on a 1.5M x 8,111 sparse matrix "
        "exceeds physical memory limits (causing Out-Of-Memory kernel crashes). Therefore, an 80:20 stratified sample of 10,000 records (8,000 train, 2,000 validation) "
        "was utilized for model fitting and hyperparameter tuning. All reported validation metrics strictly represent this controlled experiment. "
        "Importantly, full test inference on all 375,000 records in ir_test.csv was successfully executed via memory-safe 5,000-row batching."
    ))
    story.append(Spacer(1, 6))

    # -------------------------------------------------------------
    # 4. DATA UNDERSTANDING AND EDA
    # -------------------------------------------------------------
    story.append(Paragraph("4. Data Understanding and Exploratory Data Analysis (EDA)", styles['Heading1Custom']))
    story.append(Paragraph("4.1 Data Quality Audit", styles['Heading2Custom']))
    
    audit_tbl_data = [
        [Paragraph("Audit Check", styles['TableHead']), Paragraph("Observed Value", styles['TableHead']), Paragraph("Action & Engineering Justification", styles['TableHead'])],
        [Paragraph("Missing Values (Nulls)", styles['TableCell']), Paragraph("0 across all 45 columns", styles['TableCell']), Paragraph("Clean dataset; no imputation required for core fields.", styles['TableCell'])],
        [Paragraph("Duplicate Complete Rows", styles['TableCell']), Paragraph("0 duplicate rows", styles['TableCell']), Paragraph("Each observation represents a unique train journey instance.", styles['TableCell'])],
        [Paragraph("Duplicate Journey IDs", styles['TableCell']), Paragraph("0 duplicate keys", styles['TableCell']), Paragraph("journey_id is a perfectly unique primary key.", styles['TableCell'])],
        [Paragraph("Zero-Variance Features", styles['TableCell']), Paragraph("is_overloaded (constant = 0)", styles['TableCell']), Paragraph("Contains no variance across all records; dropped during preprocessing.", styles['TableCell'])],
        [Paragraph("Post-Event Leakage Fields", styles['TableCell']), Paragraph("delay_minutes, primary_delay_cause", styles['TableCell']), Paragraph("Strictly quarantined from model training matrix to prevent fatal leakage.", styles['TableCell'])]
    ]
    t_audit = Table(audit_tbl_data, colWidths=[1.8*inch, 1.8*inch, 3.4*inch])
    t_audit.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [c_light, colors.white]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_audit)
    story.append(Spacer(1, 8))

    story.append(Paragraph("4.2 Target Variable Class Distribution", styles['Heading2Custom']))
    story.append(Paragraph(
        "Analysis of the target variable is_delayed reveals significant class imbalance: 72.16% of journeys in the training dataset are delayed "
        "(arrival delay > 15 minutes), while only 27.84% arrive on time. This finding is critical: because delays represent the dominant class, "
        "a naive model predicting delayed for every train would achieve an accuracy of 72.16% without learning any genuine operational patterns. "
        "Hence, accuracy alone cannot be trusted as an evaluation metric.", styles['BodyCustom']))
    
    for f in make_img("reports/figures/eda_img_1.png", "Figure 1: Target Variable Distribution (Class Imbalance) and Continuous Delay Minutes Distribution.", w=6.4*inch, h=2.2*inch):
        story.append(f)

    story.append(Paragraph("4.3 Bivariate Exploratory Analysis", styles['Heading2Custom']))
    story.append(Paragraph("• <b>Train Priority Hierarchy:</b> Premier trains with dedicated corridor clearance—such as Vande Bharat Express (delay rate ~18%), Rajdhani Express (~24%), and Shatabdi Express (~26%)—exhibit dramatically lower delay rates than conventional Mail/Express (~76%) and unreserved Passenger Trains (~88%).", styles['BulletCustom']))
    story.append(Paragraph("• <b>Zonal Bottlenecks:</b> Northern Railway (NR), North Central Railway (NCR), and Eastern Railway (ER) experience the highest delay rates (>78%), driven by extreme track utilization (>100% capacity) along the Delhi-Howrah trunk line and severe winter fog. In contrast, Southern Railway (SR) and South Western Railway (SWR) maintain significantly better punctuality (<62% delay rate).", styles['BulletCustom']))
    story.append(Paragraph("• <b>Seasonal Impact:</b> Winter exhibits the highest delay severity due to dense fog across the Indo-Gangetic plains, reducing visibility and forcing trains to operate under automatic cautionary speed limits (often capped at 30–60 km/h). Monsoon seasons experience waterlogging, landslides in ghat sections, and signal malfunctions.", styles['BulletCustom']))
    story.append(Paragraph("• <b>Root Cause Diagnostics:</b> Among delayed journeys where cause was recorded, late incoming rake turnaround accounts for over 38% of delays, followed by track maintenance/caution orders (22%), signal failures (18%), and station congestion (14%).", styles['BulletCustom']))

    for f in make_img("reports/figures/eda_img_2.png", "Figure 2: Train Delay Rates by Train Category (left) and Administrative Railway Zone (right).", w=6.4*inch, h=2.4*inch):
        story.append(f)
    for f in make_img("reports/figures/eda_img_3.png", "Figure 3: Delay Rates Across Seasons (left) and Delay Probability vs Scheduled Distance (right).", w=6.4*inch, h=2.2*inch):
        story.append(f)
    for f in make_img("reports/figures/eda_img_4.png", "Figure 4: Breakdown of Primary Operational Delay Causes in Historical Operations.", w=6.0*inch, h=2.3*inch):
        story.append(f)
    for f in make_img("reports/figures/eda_img_5.png", "Figure 5: Correlation Heatmap of Raw Numerical Features with is_delayed.", w=5.4*inch, h=3.0*inch):
        story.append(f)

    # -------------------------------------------------------------
    # 5. DATA PREPROCESSING AND DATA LEAKAGE PREVENTION
    # -------------------------------------------------------------
    story.append(Paragraph("5. Data Preprocessing and Leakage Prevention", styles['Heading1Custom']))
    story.append(Paragraph("5.1 Data Leakage Prevention: A Critical Engineering Safeguard", styles['Heading2Custom']))
    story.append(Paragraph(
        "Data leakage occurs when predictive models inadvertently access information that would not be available in real-world deployment at the moment "
        "a prediction must be made. If leakage is present, a model appears to achieve near-perfect training and validation metrics, but fails catastrophically "
        "when deployed on truly unseen future data.", styles['BodyCustom']))
    story.append(Paragraph("• <b>1. delay_minutes:</b> This is the continuous duration of delay recorded upon journey completion. Using delay_minutes to predict is_delayed is circular reasoning, because any journey with delay_minutes > 15 is automatically delayed.", styles['BulletCustom']))
    story.append(Paragraph("• <b>2. primary_delay_cause:</b> This post-journey diagnostic label (e.g. 'Signal Failure at Junction', 'Locomotive Defect') is assigned by station controllers after the journey concludes. It cannot exist at pre-departure dispatch.", styles['BulletCustom']))
    story.append(Paragraph("<b>Action Taken:</b> Both features were strictly quarantined and removed from the feature matrix X before any model training or preprocessing fitting took place.", styles['BodyCustom']))

    story.append(Paragraph("5.2 Outlier Treatment: NumPy IQR Winsorization", styles['Heading2Custom']))
    story.append(Paragraph(
        "Extreme numerical outliers can distort linear models and inflate variance. Rather than dropping rows (which loses valuable journey data), "
        "we implemented an Interquartile Range (IQR) Winsorization method using NumPy and Pandas.", styles['BodyCustom']))
    story.append(Paragraph(
        "For a numerical feature <i>x</i>, let Q1 be the 25th percentile and Q3 be the 75th percentile. The IQR is calculated as IQR = Q3 - Q1:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>Lower Bound</b> = max(0.0, Q1 - 1.5 x IQR)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>Upper Bound</b> = Q3 + 1.5 x IQR", styles['BodyCustom']))
    story.append(Paragraph("• <b>distance_km:</b> IQR = 450.0 km. Upper bound capped at 1,466.0 km (capping 3,779 extreme records across the full sample).", styles['BulletCustom']))
    story.append(Paragraph("• <b>scheduled_travel_hours:</b> IQR = 7.55 hours. Upper bound capped at 24.9 hours (capping 1,473 extreme transcontinental runs).", styles['BulletCustom']))

    story.append(Paragraph("5.3 Stratified Train-Validation Splitting & Categorical Encoding", styles['Heading2Custom']))
    story.append(Paragraph(
        "To ensure that both partitions accurately mirror the population's 72.16% class imbalance, we performed an 80:20 stratified split "
        "(8,000 train records, 2,000 validation records) with fixed random seed 42. "
        "Categorical variables (train_type, season, zone, station category, traction) were encoded using Pandas get_dummies() with training column schema alignment. "
        "Continuous variables were standardized using Z-score scaling based solely on training statistics: <i>z = (x - mean_train) / std_train</i>.", styles['BodyCustom']))

    # -------------------------------------------------------------
    # 6. FEATURE ENGINEERING AND FEATURE SELECTION
    # -------------------------------------------------------------
    story.append(Paragraph("6. Feature Engineering and Feature Selection", styles['Heading1Custom']))
    story.append(Paragraph(
        "Machine Learning algorithms learn patterns from mathematical representations. By encoding domain-specific railway operational dynamics into "
        "derived features, we provide the algorithms with explicit signals that strongly correlate with delay propensities. We engineered 11 domain features:", styles['BodyCustom']))
    
    eng_feats = [
        ("1. avg_speed_kmh", "avg_speed_kmh = distance_km / scheduled_travel_hours", "Commercial speed. Low speed indicates congestion; high speed requires pristine tracks."),
        ("2. stops_density", "stops_density = num_scheduled_stops / (distance_km / 100.0 + 0.1)", "Halt frequency per 100 km. Frequent acceleration/braking amplifies delay risk."),
        ("3. avg_stop_distance", "avg_stop_distance = distance_km / (num_scheduled_stops + 1.0)", "Average distance between halts. Captures express vs suburban runs."),
        ("4. composite_weather_severity", "severity = season_severity_score x (1.0 + 0.5 x monsoon + 0.8 x fog)", "Compound atmospheric friction score blending seasonal severity with active monsoon/fog."),
        ("5. historical_delay_risk", "risk = (100.0 - route_historical_ontime_pct) / 100.0", "Inverts route punctuality percentage into normalized delay risk probability [0 to 1]."),
        ("6. network_vulnerability", "vuln = zone_congestion_index x (1.0 + 0.5 x is_hdn_route)", "High-density network corridor exposure multiplied by zonal track congestion."),
        ("7. rake_turnaround_risk", "turnaround_risk = incoming_rake_delay_min / (turnaround_time_min + 1.0)", "Quantifies buffer deficit when an inbound rake arrives late and must be turned around."),
        ("8. equipment_age_index", "age_index = 0.6 x loco_age_years + 0.4 x coach_age_years", "Weighted rolling stock age; captures higher traction motor defects and brake binding."),
        ("9. congestion_delay_ratio", "ratio = zone_congestion_index / (avg_speed_kmh + 1.0)", "Structural friction where heavy track congestion meets slow scheduled running speeds."),
        ("10. dep_hour_sin / cos", "sin(2 x pi x hour / 24.0) & cos(2 x pi x hour / 24.0)", "Cyclical trigonometric time encodings preserving continuous daily operational cycles.")
    ]
    for name, formula, desc in eng_feats:
        story.append(Paragraph(f"• <b>{name}:</b> <i>{formula}</i> &mdash; {desc}", styles['BulletCustom']))

    for f in make_img("reports/figures/prep_img_1.png", "Figure 6: Pearson Correlation Matrix of Engineered Features with Target Variable (is_delayed).", w=5.8*inch, h=2.5*inch):
        story.append(f)

    # -------------------------------------------------------------
    # 7. MACHINE LEARNING METHODOLOGY & BASELINE
    # -------------------------------------------------------------
    story.append(Paragraph("7. Machine Learning Methodology & Baseline Model", styles['Heading1Custom']))
    story.append(Paragraph(
        "We evaluated five foundational algorithm families: a Dummy Classifier baseline, Logistic Regression (linear boundary), "
        "Decision Tree (non-linear splits), Random Forest (bagged ensemble), and LightGBM (gradient boosting).", styles['BodyCustom']))
    
    for f in make_img("reports/figures/ml_workflow_pipeline.png", "Figure 7: Complete 8-Stage Machine Learning Workflow Pipeline.", w=6.4*inch, h=3.0*inch):
        story.append(f)

    story.append(Paragraph("8. Baseline Model & Imbalance Trap", styles['Heading2Custom']))
    story.append(Paragraph(
        "Section 8 of the college guidelines requires establishing a simple baseline model. "
        "We implemented Scikit-learn's DummyClassifier(strategy='most_frequent'). "
        "Because 72.15% of journeys in the training partition are delayed, the Dummy Classifier simply predicts delayed for 100% of cases. "
        "Its validation results were: <b>Accuracy: 0.7215, Precision: 0.7215, Recall: 1.0000, F1-Score: 0.8382, ROC-AUC: 0.5000</b>. "
        "This proves why a model reporting 72% accuracy on this dataset has achieved nothing of value: it has zero discriminatory skill (AUC = 0.50). "
        "Any credible machine learning algorithm must significantly outperform this baseline in Accuracy (>72.15%) and ROC-AUC (>>0.50).", styles['BodyCustom']))

    # -------------------------------------------------------------
    # 9. HYPERPARAMETER TUNING & MODEL COMPARISON
    # -------------------------------------------------------------
    story.append(Paragraph("9. Hyperparameter Tuning & Model Comparison", styles['Heading1Custom']))
    story.append(Paragraph(
        "Hyperparameter tuning was conducted on Random Forest and LightGBM using Scikit-learn's RandomizedSearchCV with 2-fold cross-validation "
        "optimizing for ROC-AUC:<br/>"
        "• <b>Random Forest (Tuned):</b> {'n_estimators': 80, 'max_depth': 16, 'min_samples_split': 5} &rarr; CV AUC = 0.8826<br/>"
        "• <b>LightGBM (Tuned):</b> {'learning_rate': 0.05, 'num_leaves': 63, 'max_depth': 6} &rarr; CV AUC = 0.9089", styles['BodyCustom']))
    
    story.append(Paragraph("10. Master Model Comparison Table (College Guidelines Schema)", styles['Heading2Custom']))
    
    comp_tbl_data = [
        [Paragraph("Model", styles['TableHead']), Paragraph("Best Hyperparameters", styles['TableHead']), Paragraph("Accuracy", styles['TableHead']), Paragraph("Precision", styles['TableHead']), Paragraph("Recall", styles['TableHead']), Paragraph("ROC-AUC", styles['TableHead'])],
        [Paragraph("Baseline (Dummy)", styles['TableCell']), Paragraph("strategy='most_frequent'", styles['TableCell']), Paragraph("0.7215", styles['TableCell']), Paragraph("0.7215", styles['TableCell']), Paragraph("1.0000", styles['TableCell']), Paragraph("0.5000", styles['TableCell'])],
        [Paragraph("Logistic Regression", styles['TableCell']), Paragraph("C=1.0, penalty='l2', max_iter=500", styles['TableCell']), Paragraph("0.8570", styles['TableCell']), Paragraph("0.8901", styles['TableCell']), Paragraph("0.9148", styles['TableCell']), Paragraph("0.9229", styles['TableCell'])],
        [Paragraph("Decision Tree", styles['TableCell']), Paragraph("max_depth=10, min_samples_leaf=20", styles['TableCell']), Paragraph("0.8130", styles['TableCell']), Paragraph("0.8585", styles['TableCell']), Paragraph("0.8870", styles['TableCell']), Paragraph("0.8593", styles['TableCell'])],
        [Paragraph("Random Forest (Default)", styles['TableCell']), Paragraph("n_estimators=100, max_depth=None", styles['TableCell']), Paragraph("0.7730", styles['TableCell']), Paragraph("0.7640", styles['TableCell']), Paragraph("0.9917", styles['TableCell']), Paragraph("0.8831", styles['TableCell'])],
        [Paragraph("LightGBM (Default)", styles['TableCell']), Paragraph("n_estimators=100, lr=0.1, leaves=31", styles['TableCell']), Paragraph("0.8560", styles['TableCell']), Paragraph("0.8889", styles['TableCell']), Paragraph("0.9148", styles['TableCell']), Paragraph("0.9152", styles['TableCell'])],
        [Paragraph("Random Forest (Tuned)", styles['TableCell']), Paragraph("n_est=80, max_depth=16, split=5", styles['TableCell']), Paragraph("0.7870", styles['TableCell']), Paragraph("0.7783", styles['TableCell']), Paragraph("0.9854", styles['TableCell']), Paragraph("0.8854", styles['TableCell'])],
        [Paragraph("<b>LightGBM (Champion)</b>", styles['TableCell']), Paragraph("<b>lr=0.05, leaves=63, depth=6</b>", styles['TableCell']), Paragraph("<b>0.8585</b>", styles['TableCell']), Paragraph("<b>0.8872</b>", styles['TableCell']), Paragraph("<b>0.9210</b>", styles['TableCell']), Paragraph("<b>0.9121</b>", styles['TableCell'])]
    ]
    t_comp = Table(comp_tbl_data, colWidths=[1.6*inch, 2.1*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.9*inch])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [c_light, colors.white]),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#E0F2FE")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 8))

    for f in make_img("reports/figures/model_img_1.png", "Figure 8: Comparative Receiver Operating Characteristic (ROC) Curves (left) and Confusion Matrix for Champion Tuned LightGBM (right).", w=6.4*inch, h=2.4*inch):
        story.append(f)

    story.append(Paragraph(
        "<b>Model Selection Justification:</b> Tuned LightGBM was selected as the champion model for our operational dispatch pipeline because it achieves the best balance between "
        "operational safety (92.10% recall ensures very few delayed trains are missed) and schedule efficiency (88.72% precision minimizes false alarms). "
        "While Logistic Regression achieved a slightly higher ROC-AUC (0.9229), Tuned LightGBM achieved higher overall accuracy (85.85% vs 85.70%) and recall (92.10% vs 91.48%), "
        "capturing non-linear interactions between weather severity and high-density network corridors.", styles['BodyCustom']))

    # -------------------------------------------------------------
    # 11. ERROR ANALYSIS
    # -------------------------------------------------------------
    story.append(Paragraph("11. Error Analysis", styles['Heading1Custom']))
    story.append(Paragraph(
        "Evaluating Tuned LightGBM on the 2,000 validation records yields the following confusion matrix counts:<br/>"
        "• <b>True Positives (TP = 1,329):</b> Delayed journeys correctly flagged (92.10% of all delayed trains).<br/>"
        "• <b>True Negatives (TN = 388):</b> On-time journeys correctly identified (69.66% of all on-time trains).<br/>"
        "• <b>False Positives (FP = 169):</b> On-time journeys misclassified as delayed (False Alarms; 30.34% of on-time trains).<br/>"
        "• <b>False Negatives (FN = 114):</b> Delayed journeys missed by the model (Missed Delays; 7.90% of delayed trains).", styles['BodyCustom']))
    
    for f in make_img("reports/figures/model_img_2.png", "Figure 9: Error Breakdown (False Positives and False Negatives) Grouped by Railway Zone and Train Category.", w=6.4*inch, h=2.0*inch):
        story.append(f)

    story.append(Paragraph(
        "<b>Operational Impact:</b> False negatives (missed delays) are the most critical error in train dispatching: when an unpredicted delay occurs, controllers fail to clear platforms or adjust connecting rakes, causing cascading secondary delays. "
        "False positives (false alarms) occur predominantly in high-congestion zones (NR, NCR) where trains with experienced loco pilots managed to recover lost running time.", styles['BodyCustom']))

    # -------------------------------------------------------------
    # 12. MODEL INTERPRETATION AND FEATURE IMPORTANCE
    # -------------------------------------------------------------
    story.append(Paragraph("12. Model Interpretation and Feature Importance", styles['Heading1Custom']))
    story.append(Paragraph(
        "We extracted the split-based feature importances from our trained LightGBM model. "
        "Crucially, 5 of the top 15 features are our domain-engineered features (avg_speed_kmh, network_vulnerability, equipment_age_index, composite_weather_severity, and historical_delay_risk). "
        "The single most influential feature is avg_speed_kmh (570 splits), confirming that scheduled commercial speed relative to route profile provides the strongest signal of delay vulnerability.", styles['BodyCustom']))
    
    for f in make_img("reports/figures/model_img_3.png", "Figure 10: Top 15 Most Influential Features in Tuned LightGBM Model.", w=5.8*inch, h=2.8*inch):
        story.append(f)

    # -------------------------------------------------------------
    # 13. FINAL PREDICTIONS AND DEMONSTRATION
    # -------------------------------------------------------------
    story.append(Paragraph("13. Final Predictions and Single-Journey Demonstration", styles['Heading1Custom']))
    story.append(Paragraph(
        "The champion model was deployed to generate predictions on all 375,000 unseen test journeys (ir_test.csv) in memory-safe 5,000-row batches. "
        "The output file (data/submission.csv) passed all structural audits: exactly 375,000 rows, 0 nulls, 0 duplicate keys, and valid probability range [0.0223 to 0.9949].", styles['BodyCustom']))
    
    for f in make_img("reports/figures/demo_prediction_comparison.png", "Figure 11: Real-World Demonstration Scenarios: Premier Vande Bharat Express (Green) vs Monsoon Mail/Express (Red).", w=6.2*inch, h=2.4*inch):
        story.append(f)

    story.append(Paragraph(
        "<b>Operational Triage Rules:</b> In the deployed Streamlit application (app.py), journeys are triaged into: "
        "<b>GREEN (On-Time Expected, &lt;40% probability)</b>, <b>AMBER (Moderate Delay Risk, 40%–65%)</b>, and <b>RED (High Delay Risk, &gt;65%)</b>, providing actionable dispatch directives.", styles['BodyCustom']))

    # -------------------------------------------------------------
    # 14. LIMITATIONS & 15. CONCLUSION
    # -------------------------------------------------------------
    story.append(Paragraph("14. Project Limitations", styles['Heading1Custom']))
    story.append(Paragraph("• <b>Sample Size:</b> Training was conducted on a 10,000-record sample to prevent RAM exhaustion on student workstations. While statistically consistent, full-scale cloud training could capture rare station anomalies.", styles['BulletCustom']))
    story.append(Paragraph("• <b>train_number Exclusion:</b> Excluding train_number controlled memory but eliminated individual service-specific historical track records.", styles['BulletCustom']))
    story.append(Paragraph("• <b>Static Pre-Departure Scope:</b> The model utilizes pre-departure timetable and weather data; it lacks live GPS block section telemetry and dynamic signal interlocking feeds.", styles['BulletCustom']))

    story.append(Paragraph("15. Conclusion and Future Improvements", styles['Heading1Custom']))
    story.append(Paragraph(
        "This project successfully demonstrated an end-to-end Machine Learning pipeline for train delay prediction adhering to the 19-stage PBL guidelines. "
        "We achieved 85.85% Accuracy and 92.10% Recall with Tuned LightGBM, proved the necessity of domain feature engineering, and deployed an interactive Streamlit decision support system. "
        "Future work will explore distributed cloud training on the full 1.5M dataset, native CatBoost categorical handling, and real-time NTES GPS API integration.", styles['BodyCustom']))

    # -------------------------------------------------------------
    # REFERENCES
    # -------------------------------------------------------------
    story.append(Paragraph("References", styles['Heading1Custom']))
    refs = [
        "1. Ministry of Railways, Government of India. (2024). Indian Railways Year Book & Network Punctuality Statistics. New Delhi: Railway Board.",
        "2. Kaggle Inc. (2024). Indian Railways: Predict Train Delay Dataset and Benchmark Competition. https://www.kaggle.com/",
        "3. Ke, G., Meng, Q., Finley, T., et al. (2017). LightGBM: A Highly Efficient Gradient Boosting Decision Tree. Advances in Neural Information Processing Systems (NeurIPS 30), 3146–3154.",
        "4. Pedregosa, F., Varoquaux, G., et al. (2011). Scikit-learn: Machine Learning in Python. Journal of Machine Learning Research, 12, 2825–2830.",
        "5. Breiman, L. (2001). Random Forests. Machine Learning, 45(1), 5–32.",
        "6. McKinney, W. (2010). Data Structures for Statistical Computing in Python. Proceedings of the 9th Python in Science Conference, 51–56.",
        "7. Harris, C. R., et al. (2020). Array programming with NumPy. Nature, 585, 357–362.",
        "8. Adani University. (2026). ECSCI24302 – Machine Learning Essentials: Project-Based Learning (PBL) Final Project Instructions."
    ]
    for r in refs:
        story.append(Paragraph(r, styles['BodyCustom']))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {output_path}")

if __name__ == "__main__":
    build_pdf()
