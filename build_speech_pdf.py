"""
Builds the formal PDF document for the Three-Person Live Project Demonstration Speech.
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
            self.drawString(54, 750, "Indian Railways Train Delay Prediction — 3-Person Live Demonstration Speech")
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
    c_navy = colors.HexColor("#0B2545")
    c_gold = colors.HexColor("#D4AF37")
    c_gold_dark = colors.HexColor("#B8860B")
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
        fontSize=12,
        leading=16,
        textColor=colors.white,
        spaceAfter=0
    ))
    styles.add(ParagraphStyle(
        'SlideCue',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=c_navy,
        spaceBefore=8,
        spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        'ActionCue',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=c_blue,
        spaceBefore=6,
        spaceAfter=3
    ))
    styles.add(ParagraphStyle(
        'SpokenText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
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
    story.append(Paragraph("<b>Three-Person Live Demonstration & Presentation Speech</b> | Course: ECSCI24302 Machine Learning Essentials", styles['DocSubTitle']))
    story.append(HRFlowable(width="100%", thickness=2, color=c_gold, spaceAfter=10))

    # 2. Team & Summary Metadata Table
    meta_data = [
        [Paragraph("Team Members & Roles", styles['TableHead']), Paragraph("Academic Context", styles['TableHead'])],
        [
            Paragraph("• <b>Dhruv:</b> Team Lead — Problem Definition, Dataset Scope & Predictor Demo<br/>"
                      "• <b>Darshi:</b> Team Member — Dataset Analysis, Preprocessing & Feature Engineering<br/>"
                      "• <b>Kirtan:</b> Team Member — Algorithm Benchmarks, LightGBM Tuning & Error Analysis", styles['TableCell']),
            Paragraph("• <b>Institution:</b> Faculty of Engineering & Technology, Adani University<br/>"
                      "• <b>Program:</b> B.Tech Computer Science & Engineering (2nd Year)<br/>"
                      "• <b>Target Time:</b> 7 to 9 minutes total (~2.5 to 3.0 min per speaker)<br/>"
                      "• <b>Champion Model:</b> Tuned LightGBM (Accuracy: 85.85%, Recall: 92.10%, F1: 0.9038)", styles['TableCell'])
        ]
    ]
    t_meta = Table(meta_data, colWidths=[3.5*inch, 3.5*inch])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('BACKGROUND', (0,1), (-1,-1), c_card_bg),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 12))

    # 3. Master Cue Sheet Table
    story.append(Paragraph("<b>Live Demonstration Master Cue Sheet</b>", styles['SlideCue']))
    cue_data = [
        [Paragraph("Speaker", styles['TableHead']), Paragraph("Duration", styles['TableHead']), Paragraph("PPT Slides Covered", styles['TableHead']), Paragraph("Live Streamlit App Modules Demonstrated", styles['TableHead'])],
        [Paragraph("<b>1. Dhruv</b>", styles['TableCellBold']), Paragraph("2.5 min", styles['TableCell']), Paragraph("Slide 1 (Title & Team)<br/>Slide 2 (Problem & Objectives)<br/>Slide 3 (Dataset & Quality)", styles['TableCell']), Paragraph("• Module 1: Overview & Mission Control<br/>• Module 2: Train Delay Predictor (Preset 1 & 2)", styles['TableCell'])],
        [Paragraph("<b>2. Darshi</b>", styles['TableCellBold']), Paragraph("2.5 min", styles['TableCell']), Paragraph("Slide 4 (EDA & Key Insights)<br/>Slide 5 (Preprocessing Pipeline)<br/>Slide 6 (Feature Engineering)", styles['TableCell']), Paragraph("• Module 4: Exploratory Data Analysis (EDA)<br/>• Module 5: Data Preprocessing & Pipeline<br/>• Module 6: Feature Engineering & Selection", styles['TableCell'])],
        [Paragraph("<b>3. Kirtan</b>", styles['TableCellBold']), Paragraph("3.0 min", styles['TableCell']), Paragraph("Slide 7 (Workflow & Baseline)<br/>Slide 8 (Tuning & Algorithms)<br/>Slide 9 (Comparison Table)<br/>Slide 10 (Confusion Matrix)<br/>Slide 11 (Error Analysis)<br/>Slide 12 (Conclusion & Q&A)", styles['TableCell']), Paragraph("• Module 7: Model Development & Benchmarks<br/>• Module 8: Evaluation Metrics & Confusion Matrix<br/>• Module 9: Error Analysis & Misclassifications<br/>• Module 10: Model Interpretation (Feature Imp.)", styles['TableCell'])],
    ]
    t_cue = Table(cue_data, colWidths=[1.1*inch, 0.8*inch, 2.4*inch, 2.7*inch])
    t_cue.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_card_bg]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_cue)
    story.append(Spacer(1, 14))

    # Helper function for speech box
    def add_speech_card(speaker_name, slide_cue, spoken_text, action_cues=None, banner_color=c_navy):
        card_content = []
        # Header bar
        h_table = Table([[Paragraph(f"🎙️ <b>{speaker_name}</b>", styles['SpeakerHeader'])]], colWidths=[7.0*inch])
        h_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), banner_color),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        card_content.append(h_table)

        # Body
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
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        card_content.append(b_table)
        card_content.append(Spacer(1, 10))
        return KeepTogether(card_content)

    # -------------------------------------------------------------
    # PART 1: DHRUV
    # -------------------------------------------------------------
    story.append(add_speech_card(
        "SPEAKER 1: DHRUV — INTRODUCTION & PROBLEM FORMULATION",
        "SHOW PPT SLIDE 1 & SLIDE 2 (Title, Team, Problem & Objectives)",
        "Good morning respected faculty members, evaluators, and colleagues. My name is <b>Dhruv</b>, and along with "
        "my team members <b>Darshi</b> and <b>Kirtan</b>, we present our Machine Learning project: <b>'Indian Railways "
        "Train Delay Prediction and Network Punctuality Analytics'</b>.<br/><br/>"
        "Indian Railways operates one of the busiest rail networks globally, carrying over 23 million passengers daily. "
        "However, reactive delay management leads to cascading congestion across junction points. Our objective is to "
        "formulate a proactive binary classification model predicting whether a train will experience an arrival delay "
        "exceeding <b>15 minutes</b> at its final terminus (labeled 1 for Delayed, and 0 for On-Time), adhering to "
        "official Ministry of Railways punctuality standards."
    ))

    story.append(add_speech_card(
        "SPEAKER 1: DHRUV — DATASET OVERVIEW & TARGET LEAKAGE QUARANTINE",
        "SHOW PPT SLIDE 3 (Dataset Overview & Quality Assessment)",
        "Our analysis is based on 10,000 operational records sampled from historical Indian Railways logs across 45 raw features. "
        "The empirical target distribution is naturally imbalanced: <b>72.16% delayed versus 27.84% on-time</b>.<br/><br/>"
        "Crucially, we identified post-journey features—such as <code>delay_minutes</code> and <code>primary_delay_cause</code>—which "
        "represent direct target leakage. We strictly quarantined these columns so our model only uses information available "
        "prior to train dispatch. Now, let me demonstrate our live prediction dashboard."
    ))

    story.append(add_speech_card(
        "SPEAKER 1: DHRUV — LIVE STREAMLIT APP PREDICTOR DEMONSTRATION",
        "SWITCH TO LIVE WEB APP: Module 1 (Overview) & Module 2 (Delay Predictor)",
        "Here on screen is our live Streamlit application featuring an enterprise Deep Dark and Elegant Gold UI. "
        "On the Overview dashboard, operators monitor network-wide KPIs. Let us navigate to the <b>Train Delay Predictor</b> to test two scenarios.",
        action_cues=[
            "[ACTION 1] Select Preset 1: Premier Vande Bharat Express (NR - Delhi to Varanasi, 130 km/h, clear weather, LHB rake).",
            "[CLICK] 'Run ML Delay Prediction' -> Result: 3.3% Delay Probability -> GREEN: ON-TIME EXPECTED.",
            "[ACTION 2] Select Preset 2: Howrah-Amritsar Mail in Heavy Monsoon (ER - single track, 24 stops, 88% congestion, late rake).",
            "[CLICK] 'Run ML Delay Prediction' -> Result: 98.7% Delay Probability -> RED ALERT: HIGH DELAY RISK.",
            "[HANDOVER] 'I now hand over to Darshi to explain our data preprocessing and feature engineering.'"
        ]
    ))

    # Page Break for Speaker 2
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PART 2: DARSHI
    # -------------------------------------------------------------
    story.append(add_speech_card(
        "SPEAKER 2: DARSHI — EXPLORATORY DATA ANALYSIS (EDA)",
        "SHOW PPT SLIDE 4 (Exploratory Data Analysis & Key Insights)",
        "Thank you, Dhruv. Good morning everyone, I am <b>Darshi</b>.<br/><br/>"
        "During Exploratory Data Analysis, we identified three vital operational patterns:<br/>"
        "1. <b>Kinematic Threshold:</b> Trains averaging below 50 km/h suffered an 88.4% delay rate, while trains exceeding 75 km/h maintained under 15% delay incidence.<br/>"
        "2. <b>Zonal Network Friction:</b> Northern and Eastern railway zones suffer the highest congestion (>0.85), severely impacted by winter fog.<br/>"
        "3. <b>Cascading Turnaround Impact:</b> When a shared incoming rake is delayed, downstream journey delay probability surges to 91.2%, proving that delays cascade across schedules."
    ))

    story.append(add_speech_card(
        "SPEAKER 2: DARSHI — DATA PREPROCESSING & NUMPY IQR WINSORIZATION",
        "SHOW PPT SLIDE 5 (Data Preprocessing & Pipeline Architecture)",
        "To clean and prepare the data without introducing bias, we implemented a 4-stage pipeline:<br/>"
        "• Constant zero-variance features like <code>is_overloaded</code> were eliminated.<br/>"
        "• Rather than discarding extreme journeys, we applied robust <b>NumPy IQR Winsorization</b> strictly fitted on training data: "
        "capping <code>distance_km</code> at <b>1,466 km</b> and <code>scheduled_travel_hours</code> at <b>24.9 hours</b>.<br/>"
        "• High-cardinality categoricals were one-hot encoded into 8,111 aligned sparse columns, and numerical features were standardized using training-set Z-scores."
    ))

    story.append(add_speech_card(
        "SPEAKER 2: DARSHI — FEATURE ENGINEERING & LIVE DATA DEMONSTRATION",
        "SHOW PPT SLIDE 6 & SWITCH TO LIVE WEB APP (Module 4, 5, 6)",
        "We engineered five high-impact railway domain features: <code>avg_speed_kmh</code>, <code>network_vulnerability</code>, "
        "<code>equipment_age_index</code>, <code>rake_turnaround_risk</code>, and trigonometric cyclical time encodings (<code>hour_sin</code> and <code>hour_cos</code>).",
        action_cues=[
            "[SHOW LIVE APP Module 4: EDA] Display target distribution (72/28 split) and speed-delay correlation plots.",
            "[SHOW LIVE APP Module 5: Preprocessing] Highlight the 4-stage pipeline diagram and verified IQR clipping thresholds.",
            "[SHOW LIVE APP Module 6: Feature Engineering] Walk through the mathematical formulas for network vulnerability and equipment age.",
            "[HANDOVER] 'I now pass the floor to Kirtan, who will detail our model benchmarks, LightGBM tuning, and error diagnostics.'"
        ]
    ))

    # Page Break for Speaker 3
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PART 3: KIRTAN
    # -------------------------------------------------------------
    story.append(add_speech_card(
        "SPEAKER 3: KIRTAN — WORKFLOW, BASELINE & ALGORITHM BENCHMARKS",
        "SHOW PPT SLIDE 7, 8, 9 (Machine Learning Workflow, Tuning & Comparison)",
        "Thank you, Darshi. Good morning respected evaluators, I am <b>Kirtan</b>.<br/><br/>"
        "To establish a baseline, we implemented a <b>Dummy Majority-Class Classifier</b>. Because 72.15% of journeys are delayed, "
        "the baseline achieves 72.15% accuracy and 100% recall by predicting 'Delayed' every time. However, its ROC-AUC is exactly "
        "<b>0.5000</b> and Precision is only 72.15%—it has zero discriminative intelligence.<br/><br/>"
        "We evaluated four diverse algorithms: Decision Trees, Random Forests, L2-Regularized Logistic Regression, and LightGBM. "
        "On our untouched validation set of 2,000 journeys:<br/>"
        "• Decision Tree: 81.30% Accuracy | 0.8593 ROC-AUC<br/>"
        "• Random Forest: 78.70% Accuracy | 0.8854 ROC-AUC<br/>"
        "• Logistic Regression: 85.70% Accuracy | <b>0.9229 ROC-AUC</b><br/>"
        "• <b>Tuned LightGBM (Champion):</b> <b>85.85% Accuracy | 88.72% Precision | 92.10% Recall | 0.9038 F1-Score | 0.9121 ROC-AUC</b>"
    ))

    story.append(add_speech_card(
        "SPEAKER 3: KIRTAN — CONFUSION MATRIX & ERROR ANALYSIS",
        "SHOW PPT SLIDE 10 & 11 (Confusion Matrix, Error Analysis & Limitations)",
        "In passenger railway dispatching, a <b>False Negative</b> (failing to detect a delayed train) causes severe platform gridlock, "
        "whereas a <b>False Positive</b> merely triggers precautionary monitoring. LightGBM achieves a <b>92.10% Recall</b>, successfully "
        "catching over 9 out of 10 delayed trains.<br/><br/>"
        "At threshold 0.50 across 2,000 journeys: True Positives = 1,329, True Negatives = 388, False Positives = 169 (8.45%), and "
        "False Negatives = 114 (5.70%). False Negatives primarily occurred during sudden unscheduled weather and mechanical failures "
        "that cannot be anticipated from pre-departure schedules alone."
    ))

    story.append(add_speech_card(
        "SPEAKER 3: KIRTAN — LIVE UI EVALUATION DEMO & CONCLUSION",
        "SWITCH TO LIVE WEB APP (Module 7, 8, 9, 10) & SHOW PPT SLIDE 12",
        "Let me demonstrate these evaluation tools in our web platform:",
        action_cues=[
            "[SHOW LIVE APP Module 7: Benchmarks] Point out the validation bar chart comparing Accuracy, Recall, and F1 across all models.",
            "[SHOW LIVE APP Module 8: Evaluation] Demonstrate the interactive threshold explorer slider (adjust from 0.50 down to 0.35 to push recall above 96%).",
            "[SHOW LIVE APP Module 10: Feature Importance] Highlight top tree-split drivers: avg_speed_kmh (570), network_vulnerability (309), and equipment_age_index (221).",
            "[CONCLUSION] 'To summarize: our team has developed a production-ready, leakage-free ML pipeline with 85.85% accuracy and 92.10% recall, paired with a tested 13-module operations suite. On behalf of Dhruv, Darshi, and myself, thank you. We welcome your questions.'"
        ]
    ))

    # 4. Final Quick Viva Revision Table
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Essential Viva Defense Cheat-Sheet</b>", styles['SlideCue']))
    viva_summary = [
        [Paragraph("Concept", styles['TableHead']), Paragraph("Key Project Defense & Numbers", styles['TableHead'])],
        [Paragraph("Target Definition", styles['TableCellBold']), Paragraph("Binary classification of <code>is_delayed</code> (>15 minutes arrival delay at destination terminus).", styles['TableCell'])],
        [Paragraph("Data Leakage Defense", styles['TableCellBold']), Paragraph("Quarantined <code>delay_minutes</code> and <code>primary_delay_cause</code> because they are recorded post-journey.", styles['TableCell'])],
        [Paragraph("Outlier Strategy", styles['TableCellBold']), Paragraph("NumPy IQR Winsorization on training set: capped distance at 1,466 km, hours at 24.9 hrs. Zero data rows deleted.", styles['TableCell'])],
        [Paragraph("Champion Model", styles['TableCellBold']), Paragraph("Tuned LightGBM (85.85% Acc, 88.72% Prec, 92.10% Rec, 0.9038 F1, 0.9121 AUC). Highest balanced F1-score.", styles['TableCell'])],
        [Paragraph("Confusion Matrix (n=2,000)", styles['TableCellBold']), Paragraph("TP = 1,329 | TN = 388 | FP = 169 (8.45%) | FN = 114 (5.70%). High recall minimizes costly missed delays.", styles['TableCell'])],
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
