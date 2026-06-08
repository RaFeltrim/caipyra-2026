import os
from weasyprint import HTML

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Rafael Feltrim - Curriculum Vitae</title>
    <style>
        @page {
            size: A4;
            margin: 15mm 12mm;
            background-color: #ffffff;
            @bottom-right {
                content: "Page " counter(page) " of " counter(pages);
                font-family: 'Arial', sans-serif;
                font-size: 8pt;
                color: #718096;
            }
        }
        
        *, *::before, *::after {
            box-sizing: border-box;
        }

        body {
            font-family: 'Arial', sans-serif;
            color: #1a202c;
            margin: 0;
            padding: 0;
            line-height: 1.25;
            font-size: 10pt;
        }

        .header {
            border-bottom: 2px solid #2b6cb0;
            padding-bottom: 12px;
            margin-bottom: 16px;
        }

        .name {
            font-size: 20pt;
            font-weight: bold;
            color: #1a365d;
            text-transform: uppercase;
            margin: 0 0 4px 0;
            letter-spacing: 0.5px;
        }

        .title-sub {
            font-size: 12pt;
            font-weight: bold;
            color: #2b6cb0;
            margin: 0 0 8px 0;
        }

        .contact-info {
            font-size: 9pt;
            color: #4a5568;
            margin: 0;
        }

        .contact-info span {
            margin-right: 12px;
        }

        h2 {
            font-size: 13pt;
            color: #1a365d;
            text-transform: uppercase;
            margin: 18px 0 8px 0;
            padding-left: 6px;
            border-left: 4px solid #2b6cb0;
            page-break-after: avoid;
        }

        .summary-text {
            text-align: justify;
            margin: 0 0 12px 0;
        }

        .skills-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 12px;
        }

        .skills-table td {
            padding: 4px 6px;
            vertical-align: top;
            font-size: 9.5pt;
        }

        .skills-table td.category {
            font-weight: bold;
            color: #2b6cb0;
            width: 25%;
        }

        .experience-item {
            margin-bottom: 14px;
            page-break-inside: avoid;
        }

        .job-header {
            font-size: 11pt;
            font-weight: bold;
            color: #2d3748;
            margin-bottom: 3px;
        }

        .job-meta {
            font-size: 9pt;
            color: #718096;
            margin-bottom: 6px;
            font-style: italic;
        }

        .bullet-list {
            margin: 0;
            padding-left: 18px;
        }

        .bullet-list li {
            margin-bottom: 4px;
            text-align: justify;
        }

        .education-item {
            margin-bottom: 10px;
            page-break-inside: avoid;
        }

        .edu-title {
            font-size: 10.5pt;
            font-weight: bold;
            color: #2d3748;
        }

        .edu-meta {
            font-size: 9pt;
            color: #718096;
            font-style: italic;
        }
    </style>
</head>
<body>

    <div class="header">
        <h1 class="name">Rafael Feltrim</h1>
        <div class="title-sub">Senior Quality Engineer | Data Quality & Automation Specialist</div>
        <p class="contact-info">
            <span><strong>Location:</strong> São Carlos, SP, Brazil (Open to Remote / Relocation)</span>
            <span><strong>Email:</strong> rafaelfeltrim1000@hotmail.com</span>
            <span><strong>GitHub:</strong> github.com/rafaelfeltrim</span>
        </p>
    </div>

    <h2>Professional Summary</h2>
    <p class="summary-text">
        Result-driven Quality Engineer with over 4.5 years of experience specializing in high-stability test automation architectures, Data Quality validation pipelines, and modern software paradigms. Proven track record of implementing robust testing frameworks utilizing Python, Playwright, and Selenium under Clean Architecture principles. Expert in integrating artificial intelligence (LLMs) and automated gateways into CI/CD workflows to assure pipeline observability and semantic correctness. Strongly analytical problem-solver adept at managing high-complexity engineering stacks and engineering reliable automation gates for large-scale data and software systems.
    </p>

    <h2>Core Technical Expertise</h2>
    <table class="skills-table">
        <tr>
            <td class="category">Quality Engineering</td>
            <td>Shift-Left Testing, E2E Testing, E2E UI/API Automation, Test Stability Optimization, BDD/Gherkin, Asynchronous Sync Waits, Flaky Test Elimination.</td>
        </tr>
        <tr>
            <td class="category">Data Quality & AI</td>
            <td>Data Pipeline Observability, Semantic Ingestion Verification, LLM Integration Testing, Prompt/Agent Evaluation Architecture, Validation Layers.</td>
        </tr>
        <tr>
            <td class="category">Tools & Frameworks</td>
            <td>Playwright, Selenium WebDriver, Python, PyTest, Azure AI Search, LangChain, Git, CI/CD Gateways, Cursor, Claude Code, GitHub Actions.</td>
        </tr>
        <tr>
            <td class="category">Architecture & Methods</td>
            <td>Clean Architecture, SOLID Principles, Agile/Scrum Framework, Incident Root-Cause Analysis, Metrics-Driven Quality Gateways.</td>
        </tr>
    </table>

    <h2>Professional Experience</h2>

    <div class="experience-item">
        <div class="job-header">Foursys — Mid-Senior Quality Assurance Engineer (Pleno)</div>
        <div class="job-meta">Commercial Commercial Hours Slot | Dec 2025 – Present | São Carlos, SP</div>
        <ul class="bullet-list">
            <li>Designed and executed a scalable <strong>Shift-Left Data Quality gateway</strong> using <strong>Playwright</strong> and <strong>Python</strong>, dropping overall regression test execution times by <strong>40%</strong> and efficiently mitigating corrupted data ingestion in staging environments.</li>
            <li>Engineered an automated test validation layer for sophisticated, <strong>LLM-driven workflows and agntic implementations</strong>, securing a <strong>99.2% automation stability rate</strong> via custom asynchronous smart waits, removing flaky tests.</li>
            <li>Pioneered the implementation of automated health and reliability gates within <strong>CI/CD pipelines</strong>, driving down post-deployment production bugs by <strong>35%</strong> while enforcing strict compliance with <strong>Clean Architecture</strong> patterns.</li>
            <li>Collaborated actively with engineering teams to perform deep-dive data log analysis, isolating edge-case system exceptions before code reached production environments.</li>
        </ul>
    </div>

    <div class="experience-item">
        <div class="job-header">Marketplace E-Commerce Ecosystems — Freelance Software & QA Consultant</div>
        <div class="job-meta">Night & Weekend Slots (30h/month) | Jan 2024 – Present | Remote</div>
        <ul class="bullet-list">
            <li>Developed and maintained the <strong>Executive QA View</strong> and <strong>MKP Manager</strong> tools, automating validation workflows for digital assets, semantic banner ingestion, and pricing engine logic.</li>
            <li>Designed custom testing frameworks for high-velocity e-commerce integrations, maximizing throughput validation and preventing systemic platform sync faults during heavy traffic windows.</li>
            <li>Built tailored data dashboards using modern data tools to give stakeholders comprehensive operational observability regarding product integration health and pricing calculations.</li>
        </ul>
    </div>

    <div class="experience-item">
        <div class="job-header">Tech Solutions & Specialized Services — Quality Assurance & Testing Analyst</div>
        <div class="job-meta">Prior Roles | 2021 – 2025</div>
        <ul class="bullet-list">
            <li>Led the transition from legacy manual verification scripts to robust object-oriented test code utilizing <strong>Selenium WebDriver</strong> and <strong>Python</strong>, increasing test coverage by over <strong>60%</strong>.</li>
            <li>Authored comprehensive test suites driven by BDD (Gherkin syntax), bridging communication gaps between business requirements and core technical developers.</li>
            <li>Conducted exhaustive backend data profiling and API payload validation, ensuring flawless system interaction across microservices and external payment integrations.</li>
        </ul>
    </div>

    <h2>Education & Academic Projects</h2>

    <div class="education-item">
        <span class="edu-title">IFSP (Instituto Federal de Educação, Ciência e Tecnologia de São Paulo)</span>
        <span class="edu-meta">— Bachelor of Software Engineering</span>
        <div class="edu-meta">Expected Graduation: Dec 2026 | São Carlos, SP</div>
    </div>

    <div class="education-item">
        <span class="edu-title">ICMC - USP (Instituto de Ciências Matemáticas e de Computação - Universidade de São Paulo)</span>
        <span class="edu-meta">— Special Student Graduate Program</span>
        <div class="edu-meta">Focus: Mobile Development and Advanced Networking Architectures | 1st Semester 2026 | São Carlos, SP</div>
    </div>

    <h2>Certifications & Technical Credentials</h2>
    <ul class="bullet-list">
        <li><strong>Microsoft Certified: Designing and Building Integrated AI Agent Solutions in Copilot Studio (AB-620)</strong> — <i>In Progress / Beta Pipeline</i></li>
        <li><strong>Microsoft Certified: Azure Data Fundamentals / Fabric Ecosystem</strong> — <i>Preparation Track</i></li>
        <li>Advanced Continuous Integration & Automated Deployment Gateways (GitHub Actions / DevOps)</li>
    </ul>

</body>
</html>
"""

output_pdf_path = "Rafael_Feltrim_CV.pdf"
HTML(string=html_content).write_pdf(output_pdf_path)
print(f"PDF successfully generated at: {output_pdf_path}")


