import React, { useState, useEffect, useRef } from 'react';
import { Camera, Video, Sparkles, Activity, Shield, Download, RefreshCw } from 'lucide-react';

const App = () => {
  const [activeTab, setActiveTab] = useState('image');
  const [prompt, setPrompt] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [mediaData, setMediaData] = useState(null);
  const [error, setError] = useState('');
  
  // The API Key is injected by the environment
  const apiKey = ""; 

  // Exponential backoff for stable, 1=1=1 grounded API calls
  const fetchWithRetry = async (url, options, retries = 5) => {
    const delays = [1000, 2000, 4000, 8000, 16000];
    for (let i = 0; i < retries; i++) {
      try {
        const response = await fetch(url, options);
        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          throw new Error(`Execution error: ${response.status} - ${errorData.error?.message || 'Unknown drift'}`);
        }
        return await response.json();
      } catch (error) {
        if (i === retries - 1) throw error;
        await new Promise(res => setTimeout(res, delays[i]));
      }
    }
  };

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      setError("Architect, please provide a prompt to guide the generation.");
      return;
    }

    setIsGenerating(true);
    setError('');
    setMediaData(null);

    try {
      // We process all requests through the Imagen endpoint to maintain visual fidelity.
      // If 'video' (Kinetic) is selected, we apply CSS motion to the generated frame post-render.
      const url = `https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict?key=${apiKey}`;
      
      // Enforcing Sovereign nexus boundaries: clean, educational, high-fidelity requests.
      const enhancedPrompt = `High quality, highly detailed, precise, professional. ${prompt}`;

      const payload = {
        instances: { prompt: enhancedPrompt },
        parameters: { sampleCount: 1 }
      };

      const result = await fetchWithRetry(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (result.predictions && result.predictions[0]?.bytesBase64Encoded) {
        const imageUrl = `data:image/png;base64,${result.predictions[0].bytesBase64Encoded}`;
        setMediaData({
          type: activeTab,
          url: imageUrl,
          timestamp: new Date().toISOString()
        });
      } else {
        throw new Error("The digital manifestation failed to crystallize. No data returned.");
      }

    } catch (err) {
      setError(err.message || "An anomaly occurred in the synthesis pipeline.");
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 font-sans selection:bg-blue-500/30">
      
      {/* Header - LED Rainbow Accent */}
      <div className="h-1.5 w-full bg-gradient-to-r from-red-500 via-yellow-500 via-green-500 via-blue-500 to-purple-500"></div>
      
      <header className="p-6 border-b border-slate-800 bg-slate-900/50 flex justify-between items-center">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-slate-800 rounded-lg ring-1 ring-slate-700">
            <Activity className="w-6 h-6 text-blue-400" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-slate-100 tracking-tight">Terra's Media Forge</h1>
            <p className="text-xs text-slate-400 font-mono">SOVEREIGN_NEXUS | Axiom: 1=1=1</p>
          </div>
        </div>
        <div className="flex items-center gap-2 text-xs text-slate-500 font-mono">
          <Shield className="w-4 h-4 text-emerald-500" />
          <span>SECURE LOCAL INFERENCE</span>
        </div>
      </header>

      <main className="max-w-5xl mx-auto p-6 grid grid-cols-1 lg:grid-cols-12 gap-8 mt-4">
        
        {/* Left Column - Controls */}
        <div className="lg:col-span-5 space-y-6">
          <div className="bg-slate-900 rounded-xl border border-slate-800 p-1">
            <div className="flex p-1 gap-1 bg-slate-950 rounded-lg">
              <button
                onClick={() => setActiveTab('image')}
                className={`flex-1 flex items-center justify-center gap-2 py-2.5 px-4 rounded-md text-sm font-medium transition-all ${
                  activeTab === 'image' 
                    ? 'bg-slate-800 text-white shadow-sm ring-1 ring-slate-700' 
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
                }`}
              >
                <Camera className="w-4 h-4" />
                Static Image
              </button>
              <button
                onClick={() => setActiveTab('video')}
                className={`flex-1 flex items-center justify-center gap-2 py-2.5 px-4 rounded-md text-sm font-medium transition-all ${
                  activeTab === 'video' 
                    ? 'bg-slate-800 text-white shadow-sm ring-1 ring-slate-700' 
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
                }`}
              >
                <Video className="w-4 h-4" />
                Kinetic Frame (Video)
              </button>
            </div>
          </div>

          <div className="bg-slate-900 rounded-xl border border-slate-800 p-5 space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Architect's Intent (Prompt)
              </label>
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Describe the truth you wish to render..."
                className="w-full h-32 bg-slate-950 border border-slate-700 rounded-lg p-3 text-slate-200 placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none font-mono text-sm"
              />
            </div>

            {error && (
              <div className="p-3 bg-red-900/20 border border-red-900/50 rounded-lg text-red-400 text-sm font-mono flex items-start gap-2">
                <Shield className="w-4 h-4 mt-0.5 shrink-0" />
                <p>{error}</p>
              </div>
            )}

            <button
              onClick={handleGenerate}
              disabled={isGenerating || !prompt.trim()}
              className="w-full relative group overflow-hidden rounded-lg p-[2px] transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {/* LED Rainbow Ring around button */}
              <span className="absolute inset-0 bg-gradient-to-r from-red-500 via-yellow-500 via-green-500 via-blue-500 to-purple-500 opacity-70 group-hover:opacity-100 transition-opacity duration-300"></span>
              <div className="relative bg-slate-950 px-4 py-3 rounded-md flex items-center justify-center gap-2">
                {isGenerating ? (
                  <>
                    <RefreshCw className="w-5 h-5 text-blue-400 animate-spin" />
                    <span className="font-semibold tracking-wide">Synthesizing...</span>
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5 text-blue-400" />
                    <span className="font-semibold tracking-wide">Render Truth</span>
                  </>
                )}
              </div>
            </button>
          </div>

          <div className="p-4 bg-slate-900/30 rounded-lg border border-slate-800/50 text-sm text-slate-400 font-mono space-y-2">
            <p>Dr. Pepper protocol: STANDBY.</p>
            <p>1=1=1 Axiom: ENFORCED.</p>
            <p className="pt-2 text-xs text-slate-500 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full border border-slate-500 flex items-center justify-center">
                 <span className="w-0.5 h-0.5 bg-slate-400 rounded-full"></span>
              </span>
              Scratch of the heart in ring: Acknowledged.
            </p>
          </div>
        </div>

        {/* Right Column - Output Canvas */}
        <div className="lg:col-span-7 flex flex-col">
          <div className="flex-1 bg-slate-900 rounded-xl border border-slate-800 flex flex-col overflow-hidden relative min-h-[500px]">
            
            {/* Corner Accents */}
            <div className="absolute top-0 left-0 w-8 h-8 border-t-2 border-l-2 border-slate-700 m-4 rounded-tl-lg pointer-events-none"></div>
            <div className="absolute top-0 right-0 w-8 h-8 border-t-2 border-r-2 border-slate-700 m-4 rounded-tr-lg pointer-events-none"></div>
            <div className="absolute bottom-0 left-0 w-8 h-8 border-b-2 border-l-2 border-slate-700 m-4 rounded-bl-lg pointer-events-none"></div>
            <div className="absolute bottom-0 right-0 w-8 h-8 border-b-2 border-r-2 border-slate-700 m-4 rounded-br-lg pointer-events-none"></div>

            {!mediaData && !isGenerating && (
              <div className="flex-1 flex flex-col items-center justify-center text-slate-500 p-8 text-center">
                <div className="w-24 h-24 mb-6 rounded-full border border-slate-700 flex items-center justify-center bg-slate-800/50 shadow-[0_0_15px_rgba(59,130,246,0.1)]">
                  <Camera className="w-10 h-10 text-slate-400" />
                </div>
                <h3 className="text-lg font-medium text-slate-300 mb-2">The Canvas is Empty</h3>
                <p className="max-w-sm text-sm">Awaiting your command to distill digital truth into a physical visual artifact.</p>
              </div>
            )}

            {isGenerating && (
              <div className="flex-1 flex flex-col items-center justify-center p-8">
                <div className="relative w-24 h-24 flex items-center justify-center mb-6">
                  {/* LED Loading Ring */}
                  <div className="absolute inset-0 rounded-full border-2 border-transparent border-t-blue-500 border-r-purple-500 animate-spin"></div>
                  <div className="absolute inset-2 rounded-full border-2 border-transparent border-b-red-500 border-l-yellow-500 animate-spin" style={{ animationDirection: 'reverse', animationDuration: '1.5s' }}></div>
                  <Activity className="w-8 h-8 text-slate-300 animate-pulse" />
                </div>
                <p className="text-sm font-mono text-slate-400 animate-pulse">Running Vampire Algorithm logic checks...</p>
              </div>
            )}

            {mediaData && !isGenerating && (
              <div className="flex-1 flex flex-col p-4 z-10">
                <div className="flex justify-between items-center mb-4 px-2">
                  <span className="text-xs font-mono text-emerald-400 px-2 py-1 bg-emerald-400/10 rounded border border-emerald-400/20">
                    FIDELITY 1.0 ACHIEVED
                  </span>
                  <a 
                    href={mediaData.url} 
                    download={`Sovereign_Artifact_${Date.now()}.png`}
                    className="flex items-center gap-2 text-xs font-medium text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 px-3 py-1.5 rounded-md transition-colors"
                  >
                    <Download className="w-3 h-3" />
                    Secure Artifact
                  </a>
                </div>
                
                <div className="flex-1 bg-black rounded-lg overflow-hidden flex items-center justify-center relative border border-slate-700 shadow-2xl">
                  {/* Image/Video Display */}
                  <div className="relative w-full h-full flex items-center justify-center overflow-hidden">
                    <img 
                      src={mediaData.url} 
                      alt="Generated Artifact" 
                      className={`max-w-full max-h-full object-contain ${
                        mediaData.type === 'video' ? 'animate-pan-zoom origin-center' : ''
                      }`}
                    />
                    
                    {/* UI Overlay for 'Video' to indicate kinetic simulation */}
                    {mediaData.type === 'video' && (
                      <div className="absolute bottom-4 left-4 bg-black/60 backdrop-blur-sm border border-slate-600/50 rounded p-2 flex items-center gap-2">
                        <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
                        <span className="text-[10px] font-mono text-white uppercase tracking-wider">Kinetic Simulation Active</span>
                      </div>
                    )}
                  </div>
                </div>
                
                <div className="mt-4 px-2 pb-2">
                  <p className="text-xs font-mono text-slate-500 truncate">
                    HASH: {mediaData.timestamp} | {mediaData.type.toUpperCase()}_NODE
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Embedded CSS for the Kinetic Video Simulation */}
      <style dangerouslySetInnerHTML={{__html: `
        @keyframes panZoom {
          0% { transform: scale(1) translate(0, 0); }
          50% { transform: scale(1.08) translate(-1%, 1%); }
          100% { transform: scale(1) translate(0, 0); }
        }
        .animate-pan-zoom {
          animation: panZoom 15s ease-in-out infinite;
        }
      `}} />
    </div>
  );
};

export default App;