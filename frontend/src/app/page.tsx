import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 to-violet-600 flex items-center justify-center p-4">
      <div className="max-w-4xl mx-auto text-center text-white">
        <h1 className="text-5xl font-bold mb-6">
          🔊 Scam Shield
        </h1>
        <p className="text-2xl mb-8">
          Real-Time Voice Deepfake Detection
        </p>
        <p className="text-xl mb-12 opacity-90">
          Protect yourself from AI-powered phone scams with instant analysis
        </p>

        <div className="flex gap-4 justify-center flex-wrap">
          <Link href="/login">
            <button className="bg-white text-purple-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition">
              Get Started
            </button>
          </Link>
          <Link href="/register">
            <button className="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white/10 transition">
              Sign Up Free
            </button>
          </Link>
        </div>

        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8 text-left">
          <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6">
            <h3 className="text-xl font-bold mb-2">⚡ Real-Time</h3>
            <p>Detect scams during the call, not after</p>
          </div>
          <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6">
            <h3 className="text-xl font-bold mb-2">🤖 AI-Powered</h3>
            <p>Advanced deepfake detection technology</p>
          </div>
          <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6">
            <h3 className="text-xl font-bold mb-2">📱 PWA</h3>
            <p>Install like a native app, works offline</p>
          </div>
        </div>
      </div>
    </div>
  );
}
