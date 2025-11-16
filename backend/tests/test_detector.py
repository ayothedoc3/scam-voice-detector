"""Detector service tests"""
import pytest
from app.services.detector import ResembleDetector

def test_risk_level_calculation():
    """Test risk level calculation"""
    detector = ResembleDetector()
    
    assert detector.calculate_risk_level(95) == "CRITICAL"
    assert detector.calculate_risk_level(80) == "HIGH"
    assert detector.calculate_risk_level(60) == "MEDIUM"
    assert detector.calculate_risk_level(30) == "LOW"

def test_explanation_generation():
    """Test explanation generation"""
    detector = ResembleDetector()
    
    explanation = detector.generate_explanation({}, 95)
    assert "Very high confidence" in explanation
    assert "95.0%" in explanation
    
    explanation = detector.generate_explanation({}, 75)
    assert "High confidence" in explanation
    
    explanation = detector.generate_explanation({}, 55)
    assert "Moderate confidence" in explanation
    
    explanation = detector.generate_explanation({}, 30)
    assert "Low risk" in explanation
