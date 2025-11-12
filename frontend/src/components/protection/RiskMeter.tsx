'use client';

import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';

interface RiskMeterProps {
  score: number;
  level: string;
}

export function RiskMeter({ score, level }: RiskMeterProps) {
  const getRiskColor = (level: string) => {
    switch (level) {
      case 'CRITICAL':
        return 'text-red-600';
      case 'HIGH':
        return 'text-orange-500';
      case 'MEDIUM':
        return 'text-yellow-500';
      default:
        return 'text-green-500';
    }
  };

  const getProgressColor = (score: number) => {
    if (score >= 86) return 'bg-red-600';
    if (score >= 61) return 'bg-orange-500';
    if (score >= 31) return 'bg-yellow-500';
    return 'bg-green-500';
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Risk Level</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex items-center justify-between">
          <span className="text-4xl font-bold">{score.toFixed(0)}%</span>
          <span className={`text-xl font-bold ${getRiskColor(level)}`}>
            {level}
          </span>
        </div>
        <div className="relative">
          <Progress value={score} className="h-4" />
          <div
            className={`absolute top-0 left-0 h-4 rounded-full transition-all ${getProgressColor(score)}`}
            style={{ width: `${score}%` }}
          />
        </div>
        <div className="text-sm text-muted-foreground">
          {score < 31 && 'Call appears safe'}
          {score >= 31 && score < 61 && 'Some suspicious indicators detected'}
          {score >= 61 && score < 86 && 'High probability of scam - be cautious'}
          {score >= 86 && 'CRITICAL: Strong scam indicators - end call immediately'}
        </div>
      </CardContent>
    </Card>
  );
}
