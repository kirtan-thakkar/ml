"""
Builds the formal PDF document for the Enhanced Three-Person Live Project Demonstration Speech.
Course: ECSCI24302 - Machine Learning Essentials (Adani University)
Speakers: Dhruv, Darshi, Kirtan
Output: deliverables/Three_Person_Project_Demonstration_Speech.pdf
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PDF = os.path.join(ROOT_DIR, "deliverables", "Three_Person_Project_Demonstration_Speech.pdf")


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "Indian Railways Train Delay Prediction — 3-Person Live Demonstration Script")
            self.drawRightString(612 - 54, 750, "ECSCI24302 Machine Learning Essentials")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 744, 612 - 54, 744)

        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 45, 612 - 54, 45)
        self.drawString(54, 32, "Adani University | Faculty of Engineering & Technology | Academic Year 2026–2027")
        self.drawRightString(612 - 54, 32, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def generate_speech_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    c_navy = colors.HexColor("#0B1220")
    c_surface = colors.HexColor("#111C2E")
    c_gold = colors.HexColor("#D4AF37")
    c_card_bg = colors.HexColor("#F8FAFC")
    c_speech_bg = colors.HexColor("#F1F5F9")
    c_dark_text = colors.HexColor("#0F172A")
    c_sub_text = colors.HexColor("#475569")
    c_border = colors.HexColor("#CBD5E1")
    c_green = colors.HexColor("#16A36A")
    c_red = colors.HexColor("#DC4444")
    c_blue = colors.HexColor("#2563EB")

    # Typography styles
    styles.add(ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=c_navy,
        spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=c_sub_text,
        spaceAfter=8
    ))
    styles.add(ParagraphStyle(
        'SpeakerHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.white,
        spaceAfter=0
    ))
    styles.add(ParagraphStyle(
        'SlideCue',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=c_navy,
        spaceBefore=6,
        spaceAfter=3
    ))
    styles.add(ParagraphStyle(
        'ActionCue',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=12,
        textColor=c_blue,
        spaceBefore=4,
        spaceAfter=2
    ))
    styles.add(ParagraphStyle(
        'SpokenText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=c_dark_text,
        spaceBefore=2,
        spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        'TableHead',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=1
    ))
    styles.add(ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=c_dark_text
    ))
    styles.add(ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=c_navy
    ))

    story = []

    # 1. Document Title Header
    story.append(Paragraph("INDIAN RAILWAYS TRAIN DELAY PREDICTION & PUNCTUALITY ANALYTICS", styles['DocTitle']))
    story.append(Paragraph("<b>Comprehensive Three-Person Live Demonstration Script (10–12 Minutes)</b> | Course: ECSCI24302 Machine Learning Essentials", styles['DocSubTitle']))
    story.append(HRFlowable(width="100%", thickness=2, color=c_gold, spaceAfter=8))

    # 2. Team & Summary Metadata Table
    meta_data = [
        [Paragraph("Team Members & Roles", styles['TableHead']), Paragraph("Presentation & Defense Overview", styles['TableHead'])],
        [
            Paragraph("• <b>Dhruv:</b> Team Lead — Problem Context, Solution Architecture, Dataset Scope & Live Predictor Demo<br/>"
                      "• <b>Darshi:</b> Team Member — Data Understanding, EDA Insights, Preprocessing Pipeline & Feature Engineering<br/>"
                      "• <b>Kirtan:</b> Team Member — Algorithm Selection, Tuning, Benchmarks, Confusion Matrix & Error Analysis", styles['TableCell']),
            Paragraph("• <b>Institution:</b> Faculty of Engineering & Technology, Adani University<br/>"
                      "• <b>Program:</b> B.Tech Computer Science & Engineering (2nd Year)<br/>"
                      "• <b>Total Speaking Time:</b> ~10 to 12 minutes (~3.5 to 4.0 min per speaker)<br/>"
                      "• <b>Champion Model:</b> Tuned LightGBM (Accuracy: 85.85%, Recall: 92.10%, F1: 0.9038)", styles['TableCell'])
        ]
    ]
    t_meta = Table(meta_data, colWidths=[3.5*inch, 3.5*inch])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('BACKGROUND', (0,1), (-1,-1), c_card_bg),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 10))

    # 3. Master Cue Sheet Table
    story.append(Paragraph("<b>Master Presentation & Live Demonstration Cue Sheet</b>", styles['SlideCue']))
    cue_data = [
        [Paragraph("Speaker", styles['TableHead']), Paragraph("Duration", styles['TableHead']), Paragraph("PPT Slides Covered", styles['TableHead']), Paragraph("Live Streamlit App Modules Demonstrated", styles['TableHead'])],
        [Paragraph("<b>1. Dhruv</b>", styles['TableCellBold']), Paragraph("~3.5 min", styles['TableCell']), Paragraph("• Slide 1: Cover & Team Details<br/>• Slide 2: The Problem: Reactive vs Proactive<br/>• Slide 3: The Solution: ML Architecture<br/>• Slide 4: Dataset & Quality Assurance", styles['TableCell']), Paragraph("• Module 1: Overview & Mission Control<br/>• Module 2: Train Delay Predictor<br/>  - Preset 1: Vande Bharat (3.3% On-Time)<br/>  - Preset 2: Monsoon Mail (98.7% Delayed)", styles['TableCell'])],
        [Paragraph("<b>2. Darshi</b>", styles['TableCellBold']), Paragraph("~3.5 min", styles['TableCell']), Paragraph("• Slide 5: Exploratory Data Analysis<br/>• Slide 6: Preprocessing & Pipeline Architecture", styles['TableCell']), Paragraph("• Module 4: Exploratory Data Analysis (EDA)<br/>• Module 5: Data Preprocessing & Pipeline<br/>• Module 6: Feature Engineering & Selection", styles['TableCell'])],
        [Paragraph("<b>3. Kirtan</b>", styles['TableCellBold']), Paragraph("~4.5 min", styles['TableCell']), Paragraph("• Slide 7: Model Selection & Algorithms<br/>• Slide 8: Model Comparison & Benchmarks<br/>• Slide 9: Evaluation & Confusion Matrix<br/>• Slide 10: Live Application & Presets<br/>• Slide 11: What We Learned & Limitations<br/>• Slide 12: Conclusion & Q&A Defense", styles['TableCell']), Paragraph("• Module 7: Model Development & Benchmarks<br/>• Module 8: Evaluation Metrics & Confusion Matrix<br/>• Module 9: Error Analysis & Misclassifications<br/>• Module 10: Model Interpretation (Feature Imp.)<br/>• Final closing remarks and Q&A handover", styles['TableCell'])],
    ]
    t_cue = Table(cue_data, colWidths=[1.0*inch, 0.7*inch, 2.5*inch, 2.8*inch])
    t_cue.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_card_bg]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_cue)
    story.append(Spacer(1, 10))

    # Helper function for speech box
    def add_speech_card(speaker_name, slide_cue, spoken_text, action_cues=None, banner_color=c_navy):
        card_content = []
        h_table = Table([[Paragraph(f"🎙️ <b>{speaker_name}</b>", styles['SpeakerHeader'])]], colWidths=[7.0*inch])
        h_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), banner_color),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ]))
        card_content.append(h_table)

        body_elements = []
        if slide_cue:
            body_elements.append(Paragraph(f"📌 <b>{slide_cue}</b>", styles['SlideCue']))
        
        body_elements.append(Paragraph(f"<i>&ldquo;{spoken_text}&rdquo;</i>", styles['SpokenText']))

        if action_cues:
            for act in action_cues:
                body_elements.append(Paragraph(f"⚡ <b>{act}</b>", styles['ActionCue']))

        b_table = Table([[body_elements]], colWidths=[7.0*inch])
        b_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), c_speech_bg),
            ('BOX', (0,0), (-1,-1), 0.5, c_border),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 7),
            ('RIGHTPADDING', (0,0), (-1,-1), 7),
        ]))
        card_content.append(b_table)
        card_content.append(Spacer(1, 8))
        return KeepTogether(card_content)

    # -------------------------------------------------------------
    # PART 1: DHRUV
    # -------------------------------------------------------------
    story.append(add_speech_card(
        "SPEAKER 1: DHRUV — INTRODUCTION & REAL-WORLD PROBLEM CONTEXT",
        "SHOW PPT SLIDE 1 & SLIDE 2 (Title, Team, Problem Statement)",
        "Good morning respected faculty guide, evaluators, and my fellow engineering colleagues. My name is <b>Dhruv</b>, "
        "and along with my teammates <b>Darshi</b> and <b>Kirtan</b>, we are proud to present our project: <b>'Indian Railways Train Delay "
        "Prediction and Network Punctuality Analytics'</b>.<br/><br/>"
        "Indian Railways operates one of the busiest rail networks in the world, carrying over 23 million passengers daily across 68,000 route kilometers. "
        "Yet, every passenger has experienced the frustration of unexpected delays. In traditional railway operations, delay management is almost entirely "
        "<b>reactive</b>—station masters only realize a train is delayed after it gets stuck at an outer signal, by which time platforms are blocked and connecting "
        "trains are held up in a cascading chain reaction.<br/><br/>"
        "Our machine learning objective is to transform this into <b>proactive risk forecasting</b>. Specifically, we formulate a binary classification task: "
        "predicting whether a passenger train will suffer an arrival delay exceeding <b>15 minutes</b> at its final terminus. An arrival within 15 minutes is officially "
        "classified by Indian Railways as On-Time (target = 0), while delays beyond 15 minutes are labeled Delayed (target = 1)."
    ))

    story.append(add_speech_card(
        "SPEAKER 1: DHRUV — SOLUTION ARCHITECTURE & DATASET INTEGRITY",
        "SHOW PPT SLIDE 3 & SLIDE 4 (Intelligent Architecture & Dataset Overview)",
        "On Slide 3, you can see our end-to-end architecture. Our model ingests information available <i>prior to departure</i>—scheduled travel speed, "
        "historical punctuality, weather friction, track density, and rolling stock age—processes it through our zero-leakage pipeline, and outputs calibrated delay probabilities.<br/><br/>"
        "Our data foundation is sourced from Kaggle Indian Railways operational logs comprising over 1.5 million rows across 45 raw attributes. For our experimental "
        "development and local deployment, we utilized a representative, stratified sample of <b>10,000 operational journeys</b> with an 80/20 train-validation split.<br/><br/>"
        "The empirical target distribution is naturally imbalanced: <b>72.16% delayed versus 27.84% on-time</b>, reflecting real-world track congestion. Crucially, we quarantined "
        "post-journey features like <code>delay_minutes</code> and <code>primary_delay_cause</code> so our models never suffer from target leakage. Now, let me demonstrate our live web application."
    ))

    story.append(add_speech_card(
        "SPEAKER 1: DHRUV — LIVE STREAMLIT WEB APP PREDICTOR DEMONSTRATION",
        "SWITCH TO LIVE STREAMLIT APP: Module 1 (Overview) & Module 2 (Delay Predictor)",
        "Here on screen is our live web application featuring an enterprise Deep Dark and Gold interface. On the Overview dashboard, operators see network telemetry: "
        "10,000 verified records, 8,111 sparse features, and our champion LightGBM model. Let us navigate to the <b>Train Delay Predictor</b> to test two real operational scenarios.",
        action_cues=[
            "[ACTION 1] In Preset Scenarios dropdown, click 'Preset 1: Premier Vande Bharat Express' (130 km/h, Northern Railway, clear weather, modern LHB rake, 0 min turnaround delay).",
            "[CLICK] 'Run ML Delay Prediction' -> Result: 3.3% Delay Probability -> GREEN: ON-TIME EXPECTED (System advises standard priority dispatch).",
            "[ACTION 2] In Preset Scenarios dropdown, click 'Preset 2: Howrah-Amritsar Mail in Heavy Monsoon' (38 km/h, Eastern Railway, 88% congestion, single track, 24 halts, late incoming rake).",
            "[CLICK] 'Run ML Delay Prediction' -> Result: 98.7% Delay Probability -> RED ALERT: HIGH DELAY RISK (Urgent operational advisory: alert DOM, clear turnaround buffers).",
            "[HANDOVER] 'Both predictions are logged in session history. I now hand over the presentation to Darshi for our EDA and feature engineering.'"
        ]
    ))

    # Page Break for Speaker 2
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PART 2: DARSHI
    # -------------------------------------------------------------
    story.append(add_speech_card(
        "SPEAKER 2: DARSHI — EXPLORATORY DATA ANALYSIS (EDA) & OPERATIONAL PATTERNS",
        "SHOW PPT SLIDE 5 (Exploratory Data Analysis & Key Insights)",
        "Thank you, Dhruv. Good morning respected professors and evaluators. I am <b>Darshi</b>, and I will explain how we analyzed and prepared our data for machine learning.<br/><br/>"
        "Before feeding data into any algorithm, we conducted thorough Exploratory Data Analysis to understand underlying physical patterns. On Slide 5, you see three key operational insights:<br/>"
        "1. <b>Kinematic Speed Threshold:</b> When plotting speed against delay, we found a stark threshold. Trains averaging below <b>50 km/h</b> had an <b>88.4% delay probability</b>, "
        "because slow services get repeatedly looped and overtaken by express trains. Conversely, trains maintaining over <b>75 km/h</b> experienced less than 15% delay incidence.<br/>"
        "2. <b>Zonal Network Friction:</b> Northern Railway (NR), North Central (NCR), and Eastern Railway (ER) experience congestion indices above 0.85, exacerbated by dense winter fog in the Indo-Gangetic plains.<br/>"
        "3. <b>Cascading Turnaround Impact:</b> When an incoming train is delayed and shares its rake with a departing service (<code>late_incoming_rake = 1</code>), outbound delay probability surges to <b>91.2%</b>."
    ))

    story.append(add_speech_card(
        "SPEAKER 2: DARSHI — DATA PREPROCESSING, IQR WINSORIZATION & FEATURE ENGINEERING",
        "SHOW PPT SLIDE 6 (Data Preprocessing & Pipeline Architecture)",
        "To clean and prepare the data reliably, we built a 4-stage pipeline using pure Pandas and NumPy:<br/>"
        "• <b>Cleaning & ID Removal:</b> Constant zero-variance columns like <code>is_overloaded</code> and raw string dates were purged.<br/>"
        "• <b>NumPy IQR Winsorization:</b> Rather than deleting extreme journeys like the 4,000-km Vivek Express—which would discard valuable long-distance data—we applied "
        "IQR Winsorization fitted strictly on training data: capping <code>distance_km</code> at <b>1,466 km</b> and <code>scheduled_travel_hours</code> at <b>24.9 hours</b>. Zero rows deleted.<br/>"
        "• <b>Domain Feature Engineering:</b> We engineered 5 high-impact features: <code>avg_speed_kmh</code>, <code>network_vulnerability</code>, <code>equipment_age_index</code>, "
        "<code>rake_turnaround_risk</code>, and cyclical trigonometric time encodings (<code>hour_sin</code> and <code>hour_cos</code>) to capture that hour 23 and 0 are consecutive.<br/>"
        "• <b>Encoding & Scaling:</b> Categorical variables were one-hot encoded into 8,111 aligned sparse columns, and continuous features were standardized using training-set Z-scores."
    ))

    story.append(add_speech_card(
        "SPEAKER 2: DARSHI — LIVE WEB APP DATA PIPELINE DEMONSTRATION",
        "SWITCH TO LIVE STREAMLIT APP: Module 4 (EDA), Module 5 (Preprocessing) & Module 6 (Feature Eng.)",
        "Let me demonstrate these preparation steps directly in our web application.",
        action_cues=[
            "[SHOW LIVE APP Module 4: EDA] Display target distribution (72.16% delayed vs 27.84% on-time) and feature correlation matrix.",
            "[SHOW LIVE APP Module 5: Preprocessing] Highlight the 4-stage pipeline diagram and verified IQR Winsorization clipping thresholds.",
            "[SHOW LIVE APP Module 6: Feature Engineering] Walk through the mathematical formulas for network vulnerability and equipment age index.",
            "[HANDOVER] 'With our dataset thoroughly cleaned and encoded into 8,111 aligned columns, it was ready for modeling. I now pass the floor to Kirtan.'"
        ]
    ))

    # Page Break for Speaker 3
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PART 3: KIRTAN
    # -------------------------------------------------------------
    story.append(add_speech_card(
        "SPEAKER 3: KIRTAN — MODEL SELECTION, TUNING & PERFORMANCE BENCHMARKS",
        "SHOW PPT SLIDE 7 & SLIDE 8 (Algorithms Tested & Benchmark Comparison)",
        "Thank you, Darshi. Good morning respected evaluators, I am <b>Kirtan</b>.<br/><br/>"
        "To establish a reference benchmark, we built a <b>Dummy Majority-Class Classifier</b>. Because 72.15% of journeys are delayed, predicting 'Delayed' every time "
        "yields 72.15% accuracy and 100% recall, but has a ROC-AUC of exactly <b>0.5000</b> and Precision of only 72.15%—it has zero discriminative power. Any viable ML model had to beat this.<br/><br/>"
        "We evaluated four distinct algorithms on our untouched validation set of 2,000 journeys:<br/>"
        "• Decision Tree: 81.30% Acc | 0.8593 ROC-AUC<br/>"
        "• Random Forest: 78.70% Acc | 0.8854 ROC-AUC<br/>"
        "• Logistic Regression (L2): 85.70% Acc | <b>0.9229 ROC-AUC</b><br/>"
        "• <b>Tuned LightGBM (Champion):</b> <b>85.85% Accuracy | 88.72% Precision | 92.10% Recall | 0.9038 F1-Score | 0.9121 ROC-AUC</b><br/><br/>"
        "On an imbalanced dataset, the <b>F1-score is the gold standard metric</b> because it balances precision and recall. LightGBM delivered the highest accuracy, highest recall, and highest F1-score."
    ))

    story.append(add_speech_card(
        "SPEAKER 3: KIRTAN — CONFUSION MATRIX, ERROR ANALYSIS & OPERATIONAL IMPACT",
        "SHOW PPT SLIDE 9 & SLIDE 10 (Confusion Matrix, Error Diagnostics & Presets)",
        "Looking at the Confusion Matrix for LightGBM across 2,000 validation journeys at a standard 0.50 threshold:<br/>"
        "• <b>True Positives:</b> 1,329 delayed trains correctly flagged.<br/>"
        "• <b>True Negatives:</b> 388 on-time trains correctly cleared.<br/>"
        "• <b>False Positives:</b> 169 trains (8.45% error rate) — triggers precautionary monitoring (low operational cost).<br/>"
        "• <b>False Negatives:</b> 114 trains (5.70% error rate) — missed delays.<br/><br/>"
        "In passenger railway dispatching, a <b>False Negative is far more hazardous than a False Positive</b>. Missing a delayed train creates unannounced platform gridlock, "
        "whereas a False Positive merely prompts precautionary checks. Achieving a <b>92.10% Recall</b> ensures that over 9 out of 10 delayed trains are caught in advance.<br/><br/>"
        "Our error analysis revealed that the 114 False Negatives were caused by sudden external failures (overhead wire tripping, unscheduled freight precedence) that cannot be predicted from scheduled timetables alone."
    ))

    story.append(add_speech_card(
        "SPEAKER 3: KIRTAN — LIVE UI EVALUATION DEMO, LIMITATIONS & CONCLUSION",
        "SHOW PPT SLIDE 11 & SLIDE 12 & SWITCH TO LIVE STREAMLIT APP",
        "Let me demonstrate these evaluation tools in our web platform:",
        action_cues=[
            "[SHOW LIVE APP Module 7: Benchmarks] Show validation bar chart comparing Accuracy, Recall, and F1 across all models.",
            "[SHOW LIVE APP Module 8: Evaluation] Demonstrate interactive threshold explorer (adjust threshold to 0.35 to push recall above 96%).",
            "[SHOW LIVE APP Module 10: Feature Importance] Highlight top tree-split drivers: avg_speed_kmh (570), network_vulnerability (309), and equipment_age_index (221).",
            "[LIMITATIONS & ROADMAP] 'Limitations: Operates on pre-departure schedules; does not ingest mid-journey GPS. Future roadmap: Integration with live NTES GPS feeds and IoT track sensors.'",
            "[CLOSING] 'To conclude: we have built an end-to-end ML solution with 85.85% accuracy, 92.10% recall, zero data leakage, and a production-grade 13-module operations suite. On behalf of Dhruv, Darshi, and myself, thank you. We are ready for your questions.'"
        ]
    ))

    # 4. Final Quick Viva Defense Cheat-Sheet
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Essential Viva Voce Defense Cheat-Sheet</b>", styles['SlideCue']))
    viva_summary = [
        [Paragraph("Topic / Question", styles['TableHead']), Paragraph("Precise Engineering Defense & Verified Metric", styles['TableHead'])],
        [Paragraph("Target Formulation", styles['TableCellBold']), Paragraph("Binary classification of <code>is_delayed</code> (>15 minutes arrival delay at destination terminus), matching MoR standards.", styles['TableCell'])],
        [Paragraph("Target Leakage Prevention", styles['TableCellBold']), Paragraph("Quarantined post-journey outcomes (<code>delay_minutes</code>, <code>primary_delay_cause</code>). Preprocessing fitted strictly on train data.", styles['TableCell'])],
        [Paragraph("Outlier Treatment", styles['TableCellBold']), Paragraph("NumPy IQR Winsorization on training set: capped distance at 1,466 km, hours at 24.9 hrs. Zero data rows discarded.", styles['TableCell'])],
        [Paragraph("Champion Model Selection", styles['TableCellBold']), Paragraph("Tuned LightGBM (85.85% Acc, 88.72% Prec, 92.10% Rec, 0.9038 F1, 0.9121 AUC). Highest balanced F1-score on imbalanced data.", styles['TableCell'])],
        [Paragraph("Recall vs Precision Trade-off", styles['TableCellBold']), Paragraph("High 92.10% Recall catches 92/100 delayed trains; False Negatives (5.7%) are far more costly to platform operations than False Positives.", styles['TableCell'])],
    ]
    t_viva = Table(viva_summary, colWidths=[1.8*inch, 5.2*inch])
    t_viva.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_card_bg]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_viva)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {OUTPUT_PDF}")


if __name__ == '__main__':
    generate_speech_pdf()
