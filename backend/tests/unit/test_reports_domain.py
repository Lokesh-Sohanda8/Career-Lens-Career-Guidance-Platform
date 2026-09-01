from app.domains.reports.models import Report, ReportSection


def test_reports_domain_models_are_available():
    assert Report.__tablename__ == "reports"
    assert ReportSection.__tablename__ == "report_sections"
