import librosa
import numpy as np
import io
import logging

logger = logging.getLogger(__name__)


class VoiceAnalyzer:
    """Analyzes voice characteristics"""

    def __init__(self):
        self.sample_rate = 16000

    async def analyze(self, audio_data: bytes) -> dict:
        """
        Analyze voice characteristics

        Returns synthetic score and voice features
        """
        try:
            # Load audio
            y, sr = librosa.load(io.BytesIO(audio_data), sr=self.sample_rate)

            # Extract features
            features = {}

            # Pitch analysis
            pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
            pitch_values = []
            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                pitch = pitches[index, t]
                if pitch > 0:
                    pitch_values.append(pitch)

            if pitch_values:
                features['pitch_mean'] = float(np.mean(pitch_values))
                features['pitch_std'] = float(np.std(pitch_values))
            else:
                features['pitch_mean'] = 0.0
                features['pitch_std'] = 0.0

            # Spectral features
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            features['spectral_centroid_mean'] = float(np.mean(spectral_centroids))
            features['spectral_centroid_std'] = float(np.std(spectral_centroids))

            # Zero crossing rate
            zcr = librosa.feature.zero_crossing_rate(y)[0]
            features['zero_crossing_rate'] = float(np.mean(zcr))

            # Energy
            rms = librosa.feature.rms(y=y)[0]
            features['energy_mean'] = float(np.mean(rms))
            features['energy_std'] = float(np.std(rms))

            # Calculate synthetic score
            synthetic_score = self._calculate_synthetic_score(features)
            features['synthetic_score'] = synthetic_score

            return features

        except Exception as e:
            logger.error(f"Voice analysis error: {str(e)}")
            return {'synthetic_score': 0.0, 'error': str(e)}

    def _calculate_synthetic_score(self, features: dict) -> float:
        """Calculate likelihood of synthetic voice"""
        score = 0.0

        # AI voices tend to have very consistent pitch
        pitch_std = features.get('pitch_std', 0)
        if pitch_std < 20:
            score += 25

        # Spectral consistency
        spec_std = features.get('spectral_centroid_std', 0)
        if spec_std < 200:
            score += 20

        # Energy consistency
        energy_std = features.get('energy_std', 0)
        if energy_std < 0.01:
            score += 20

        # Zero crossing rate
        zcr = features.get('zero_crossing_rate', 0)
        if not (0.05 < zcr < 0.15):
            score += 15

        return max(0, min(100, score))
