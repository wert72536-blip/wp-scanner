import time
from typing import List
from core.base_detector import Finding

SEVERITY_WEIGHTS = {
    'critical': 10,
    'high': 5,
    'medium': 2,
    'low': 1,
    'info': 0
}

def calculate_risk_score(findings: List[Finding]) -> int:
    if not findings:
        return 0
    raw = sum(SEVERITY_WEIGHTS.get(f.severity, 0) for f in findings)
    # Cap at 100 (arbitrary scale)
    return min(100, raw * 2)  # multiplier to spread range

def generate_report(target_url: str, findings: List[Finding]) -> dict:
    issues = []
    for f in findings:
        issues.append({
            "category": f.category,
            "severity": f.severity,
            "description": f.description,
            "recommendation": f.recommendation
        })
    risk_score = calculate_risk_score(findings)
    report = {
        "scan_target": target_url,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "risk_score": risk_score,
        "severity_summary": {
            "critical": sum(1 for f in findings if f.severity == 'critical'),
            "high": sum(1 for f in findings if f.severity == 'high'),
            "medium": sum(1 for f in findings if f.severity == 'medium'),
            "low": sum(1 for f in findings if f.severity == 'low'),
            "info": sum(1 for f in findings if f.severity == 'info')
        },
        "issues": issues
    }
    return report