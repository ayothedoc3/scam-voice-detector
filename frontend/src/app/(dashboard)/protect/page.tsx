'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { RiskMeter } from '@/components/protection/RiskMeter';
import { useProtection } from '@/lib/hooks/useProtection';

export default function ProtectPage() {
  const [phoneNumber, setPhoneNumber] = useState('');
  const [bridgeNumber, setBridgeNumber] = useState('');
  const [error, setError] = useState('');
  const { startProtection, stopProtection, isActive, riskScore, riskLevel, transcript, alerts } = useProtection();

  const handleStart = async () => {
    if (!phoneNumber) {
      setError('Please enter your phone number');
      return;
    }

    try {
      setError('');
      const response = await startProtection(phoneNumber);
      setBridgeNumber(response.bridge_number);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to start protection');
    }
  };

  const handleStop = () => {
    stopProtection();
    setBridgeNumber('');
    setPhoneNumber('');
  };

  return (
    <div className="container mx-auto p-6 max-w-4xl">
      <h1 className="text-3xl font-bold mb-6">🛡️ Call Protection</h1>

      {!isActive ? (
        <Card>
          <CardHeader>
            <CardTitle>Start Protection</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-muted-foreground">
              Enter your phone number to receive protection instructions
            </p>
            <div className="flex gap-4">
              <Input
                type="tel"
                placeholder="+1234567890"
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value)}
                className="flex-1"
              />
              <Button onClick={handleStart} size="lg">
                Start Protection
              </Button>
            </div>
            {error && (
              <p className="text-destructive text-sm">{error}</p>
            )}
            <div className="bg-muted p-4 rounded-lg">
              <h3 className="font-semibold mb-2">How it works:</h3>
              <ol className="list-decimal list-inside space-y-1 text-sm">
                <li>Enter your phone number and click Start Protection</li>
                <li>You'll receive a call from our system</li>
                <li>Answer it, then use your phone's "Add Call" or "Merge" feature</li>
                <li>Add the suspicious caller to create a three-way call</li>
                <li>We'll analyze the audio in real-time and alert you if it's a scam</li>
              </ol>
            </div>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-6">
          <Card className="border-green-500 bg-green-50">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-xl font-bold text-green-700 mb-2">🔴 Protection Active</h2>
                  <p className="text-green-600 mb-2">
                    Bridge Number: <span className="font-mono font-bold">{bridgeNumber}</span>
                  </p>
                  <p className="text-sm text-green-600">
                    Add your suspicious caller to this number using your phone's "Add Call" feature
                  </p>
                </div>
                <Button onClick={handleStop} variant="outline">
                  Stop Protection
                </Button>
              </div>
            </CardContent>
          </Card>

          <RiskMeter score={riskScore} level={riskLevel} />

          {alerts.length > 0 && (
            <Card className="border-red-500 bg-red-50">
              <CardHeader>
                <CardTitle className="text-red-700">⚠️ Alerts</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {alerts.map((alert, idx) => (
                    <div key={idx} className="p-3 bg-red-100 rounded-lg">
                      <p className="font-bold text-red-700">{alert.message}</p>
                      <p className="text-sm text-red-600">Risk Level: {alert.risk_level}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {transcript.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle>Live Transcript</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2 max-h-64 overflow-y-auto">
                  {transcript.map((entry, idx) => (
                    <div key={idx} className="border-l-2 border-gray-300 pl-3">
                      <span className="text-xs text-muted-foreground">{entry.timestamp}</span>
                      <p className="text-sm">{entry.text}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      )}
    </div>
  );
}
