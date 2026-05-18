"use client";

import React, { useState, useRef, useEffect } from "react";
import { 
  Send, Bot, User, Settings, UploadCloud, 
  Trash2, FileText, ChevronRight, Menu, X, CheckCircle2, AlertCircle
} from "lucide-react";

type Message = {
  role: "user" | "assistant";
  content: string;
};

export default function ChatApp() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "Hello! I am your AI Customer Support assistant. Upload your documents in the sidebar, provide your API key, and ask me anything.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  // Settings state
  const [provider, setProvider] = useState("OpenAI");
  const [apiKey, setApiKey] = useState("");
  const [demoCount, setDemoCount] = useState(0);

  // Upload state
  const [file, setFile] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState<"idle" | "uploading" | "success" | "error">("idle");
  const [uploadMessage, setUploadMessage] = useState("");

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api";

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!input.trim()) return;

    if (!apiKey && demoCount >= 5) {
      setMessages(prev => [...prev, { role: "assistant", content: "⚠️ Demo limit of 5 messages reached. Please provide an API key in the sidebar to continue." }]);
      return;
    }

    const userMsg = input.trim();
    setInput("");
    setMessages(prev => [...prev, { role: "user", content: userMsg }]);
    setLoading(true);

    try {
      const recentHistory = messages.slice(-5);
      const res = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query: userMsg,
          history: recentHistory,
          provider: provider.toLowerCase(),
          api_key: apiKey
        })
      });

      const data = await res.json();
      
      if (res.ok) {
        setMessages(prev => [...prev, { role: "assistant", content: data.answer }]);
        if (!apiKey) setDemoCount(c => c + 1);
      } else {
        setMessages(prev => [...prev, { role: "assistant", content: `**Error:** ${data.detail || "Server Error"}` }]);
      }
    } catch (err) {
      setMessages(prev => [...prev, { role: "assistant", content: "**Connection Error:** Could not connect to the backend server. Is FastAPI running on port 8000?" }]);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0];
    if (!selected) return;
    setFile(selected);
    setUploadStatus("idle");
  };

  const processFile = async () => {
    if (!file) return;
    
    setUploadStatus("uploading");
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`${API_URL}/documents/upload`, {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      if (res.ok) {
        setUploadStatus("success");
        setUploadMessage(`Processed ${data.chunks_added} chunks.`);
      } else {
        setUploadStatus("error");
        setUploadMessage(data.detail || "Upload failed");
      }
    } catch (err) {
      setUploadStatus("error");
      setUploadMessage("Could not connect to server.");
    }
  };

  const resetChat = () => {
    setMessages([
      {
        role: "assistant",
        content: "Hello! I am your AI Customer Support assistant. Upload your documents in the sidebar, provide your API key, and ask me anything.",
      },
    ]);
    setDemoCount(0);
  };

  return (
    <div className="flex h-screen bg-gray-950 text-gray-100 font-sans overflow-hidden">
      
      {/* Mobile Sidebar Overlay */}
      {!sidebarOpen && (
        <button 
          onClick={() => setSidebarOpen(true)}
          className="absolute top-4 left-4 z-50 p-2 bg-gray-800 rounded-md md:hidden hover:bg-gray-700 transition"
        >
          <Menu size={20} />
        </button>
      )}

      {/* Sidebar */}
      <div 
        className={`${sidebarOpen ? "translate-x-0 w-80" : "-translate-x-full w-0"} 
        transition-all duration-300 ease-in-out fixed md:relative z-40 h-full bg-gray-900 border-r border-gray-800 flex flex-col`}
      >
        <div className="flex items-center justify-between p-5 border-b border-gray-800">
          <div className="flex items-center gap-2">
            <Bot className="text-blue-500" size={24} />
            <h1 className="font-semibold text-lg tracking-tight">AI Agent</h1>
          </div>
          <button onClick={() => setSidebarOpen(false)} className="p-1 md:hidden hover:bg-gray-800 rounded">
            <X size={20} />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-5 space-y-8">
          {/* Settings Section */}
          <section className="space-y-4">
            <div className="flex items-center gap-2 text-gray-400 mb-2">
              <Settings size={18} />
              <h2 className="text-sm font-medium uppercase tracking-wider">Configuration</h2>
            </div>
            
            <div className="space-y-3">
              <div>
                <label className="block text-xs text-gray-400 mb-1">LLM Provider</label>
                <select 
                  value={provider}
                  onChange={(e) => setProvider(e.target.value)}
                  className="w-full bg-gray-950 border border-gray-800 rounded-lg p-2.5 text-sm focus:outline-none focus:border-blue-500 transition"
                >
                  <option>OpenAI</option>
                  <option>Groq</option>
                </select>
              </div>
              
              <div>
                <label className="block text-xs text-gray-400 mb-1">API Key</label>
                <input 
                  type="password"
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                  placeholder="sk-..."
                  className="w-full bg-gray-950 border border-gray-800 rounded-lg p-2.5 text-sm focus:outline-none focus:border-blue-500 transition"
                />
              </div>
            </div>
          </section>

          {/* Knowledge Base Section */}
          <section className="space-y-4">
            <div className="flex items-center gap-2 text-gray-400 mb-2">
              <FileText size={18} />
              <h2 className="text-sm font-medium uppercase tracking-wider">Knowledge Base</h2>
            </div>
            
            <div className="space-y-3">
              <label className="flex flex-col items-center justify-center w-full h-32 border-2 border-gray-800 border-dashed rounded-lg cursor-pointer bg-gray-950 hover:bg-gray-900 transition hover:border-gray-600">
                <div className="flex flex-col items-center justify-center pt-5 pb-6">
                  <UploadCloud className="w-8 h-8 mb-2 text-gray-500" />
                  <p className="mb-1 text-sm text-gray-400"><span className="font-semibold">Click to upload</span></p>
                  <p className="text-xs text-gray-500">PDF or TXT</p>
                </div>
                <input type="file" accept=".pdf,.txt" className="hidden" onChange={handleFileUpload} />
              </label>

              {file && (
                <div className="bg-gray-950 border border-gray-800 p-3 rounded-lg flex items-center justify-between">
                  <div className="flex items-center gap-2 overflow-hidden">
                    <FileText size={16} className="text-blue-500 shrink-0" />
                    <span className="text-sm truncate text-gray-300">{file.name}</span>
                  </div>
                  <button 
                    onClick={() => { setFile(null); setUploadStatus("idle"); }}
                    className="text-gray-500 hover:text-red-400 p-1"
                  >
                    <X size={14} />
                  </button>
                </div>
              )}

              <button 
                onClick={processFile}
                disabled={!file || uploadStatus === "uploading"}
                className="w-full py-2.5 px-4 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-800 disabled:text-gray-500 disabled:cursor-not-allowed text-white text-sm font-medium rounded-lg transition-colors flex justify-center items-center gap-2"
              >
                {uploadStatus === "uploading" ? (
                  <span className="animate-pulse">Processing...</span>
                ) : (
                  <>Process Document</>
                )}
              </button>

              {uploadStatus === "success" && (
                <div className="flex items-start gap-2 text-emerald-400 text-xs p-2 bg-emerald-400/10 rounded-md">
                  <CheckCircle2 size={14} className="shrink-0 mt-0.5" />
                  <span>{uploadMessage}</span>
                </div>
              )}
              {uploadStatus === "error" && (
                <div className="flex items-start gap-2 text-red-400 text-xs p-2 bg-red-400/10 rounded-md">
                  <AlertCircle size={14} className="shrink-0 mt-0.5" />
                  <span>{uploadMessage}</span>
                </div>
              )}
            </div>
          </section>
        </div>

        <div className="p-5 border-t border-gray-800">
          <button 
            onClick={resetChat}
            className="flex items-center justify-center gap-2 w-full py-2.5 px-4 bg-gray-950 hover:bg-red-500/10 hover:text-red-400 border border-gray-800 text-gray-300 text-sm font-medium rounded-lg transition-colors"
          >
            <Trash2 size={16} />
            Reset Chat
          </button>
        </div>
      </div>

      {/* Main Chat Area */}
      <main className="flex-1 flex flex-col h-full bg-[#0a0a0a] relative w-full">
        {/* Header */}
        <header className="h-16 border-b border-gray-800 flex items-center px-6 justify-between bg-gray-900/50 backdrop-blur-md sticky top-0 z-10 w-full">
          <div className="flex items-center gap-3">
            {sidebarOpen ? null : (
              <button onClick={() => setSidebarOpen(true)} className="p-1 hidden md:block hover:bg-gray-800 rounded transition text-gray-400">
                <ChevronRight size={20} />
              </button>
            )}
            <div>
              <h2 className="font-medium text-gray-200">Customer Support</h2>
              <p className="text-xs text-gray-500 flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                FastAPI Connected
              </p>
            </div>
          </div>
        </header>

        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto p-4 md:p-8 scroll-smooth pb-32">
          <div className="max-w-3xl mx-auto space-y-6">
            {messages.map((msg, idx) => (
              <div 
                key={idx} 
                className={`flex gap-4 ${msg.role === "user" ? "flex-row-reverse" : ""}`}
              >
                <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${
                  msg.role === "user" ? "bg-blue-600" : "bg-emerald-600"
                }`}>
                  {msg.role === "user" ? <User size={16} /> : <Bot size={16} />}
                </div>
                
                <div className={`px-4 py-3 rounded-2xl max-w-[85%] ${
                  msg.role === "user" 
                    ? "bg-blue-600 text-white rounded-tr-sm" 
                    : "bg-gray-800 text-gray-200 border border-gray-700 rounded-tl-sm shadow-sm"
                }`}>
                  <p className="whitespace-pre-wrap text-[15px] leading-relaxed">{msg.content}</p>
                </div>
              </div>
            ))}
            
            {loading && (
              <div className="flex gap-4">
                <div className="w-8 h-8 rounded-full bg-emerald-600 flex items-center justify-center shrink-0">
                  <Bot size={16} />
                </div>
                <div className="px-5 py-4 rounded-2xl bg-gray-800 border border-gray-700 rounded-tl-sm flex items-center gap-1.5">
                  <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                  <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                  <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input Area */}
        <div className="absolute bottom-0 left-0 w-full p-4 md:p-6 bg-gradient-to-t from-[#0a0a0a] via-[#0a0a0a] to-transparent pt-12">
          <div className="max-w-3xl mx-auto">
            <form 
              onSubmit={handleSendMessage}
              className="relative flex items-center bg-gray-800 border border-gray-700 rounded-full shadow-lg focus-within:ring-2 focus-within:ring-blue-500/50 focus-within:border-blue-500 transition-all overflow-hidden"
            >
              <input 
                type="text" 
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask about your documents..." 
                className="w-full bg-transparent border-none py-4 pl-6 pr-14 text-gray-200 placeholder-gray-500 focus:outline-none focus:ring-0 text-[15px]"
                disabled={loading}
              />
              <button 
                type="submit" 
                disabled={!input.trim() || loading}
                className="absolute right-2 p-2.5 bg-blue-600 hover:bg-blue-500 disabled:bg-gray-700 disabled:text-gray-500 text-white rounded-full transition-colors flex items-center justify-center"
              >
                <Send size={18} className="ml-0.5" />
              </button>
            </form>
            <p className="text-center text-xs text-gray-600 mt-3">
              AI Agents can make mistakes. Always verify important information.
            </p>
          </div>
        </div>
      </main>
      
    </div>
  );
}
