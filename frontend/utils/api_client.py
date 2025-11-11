"""API client for backend communication"""
import requests
import os
from typing import Dict, List
import streamlit as st

class APIClient:
    """Client for backend API"""

    def __init__(self):
        self.base_url = os.getenv("BACKEND_URL", "http://localhost:8000")
        self.api_url = f"{self.base_url}/api/v1"

    def analyze_audio(self, uploaded_file) -> Dict:
        """Send audio file for analysis"""
        files = {'file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}

        response = requests.post(
            f"{self.api_url}/analyze",
            files=files,
            timeout=60
        )

        if response.status_code != 200:
            raise Exception(f"API Error: {response.status_code} - {response.text}")

        return response.json()

    def analyze_batch(self, files: List) -> Dict:
        """Send multiple files for batch analysis"""
        files_data = [
            ('files', (f.name, f.getvalue(), f.type))
            for f in files
        ]

        response = requests.post(
            f"{self.api_url}/analyze/batch",
            files=files_data,
            timeout=180
        )

        if response.status_code != 200:
            raise Exception(f"API Error: {response.status_code} - {response.text}")

        return response.json()

    def health_check(self) -> Dict:
        """Check API health"""
        response = requests.get(f"{self.api_url}/health", timeout=5)
        return response.json()
