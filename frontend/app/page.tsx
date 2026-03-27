"use client";

import { FormEvent, useState } from "react";

const tabs = ["Home", "Geospatial Insights", "AI Itinerary", "Data Explorer"];

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8001";

export default function HomePage() {
  const [instagramUrl, setInstagramUrl] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [statusMessage, setStatusMessage] = useState("");

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setStatusMessage("");

    if (!instagramUrl.trim()) {
      setStatusMessage("Please paste an Instagram link first.");
      return;
    }

    setIsSubmitting(true);

    try {
      const response = await fetch(`${API_BASE_URL}/upload_link`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ instagram_url: instagramUrl.trim() }),
      });

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
      }

      const data = (await response.json()) as { message?: string };
      setStatusMessage(data.message ?? "Link submitted successfully.");
    } catch {
      setStatusMessage("Could not reach backend. Confirm API is running on port 8001.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <main className="min-h-screen">
      <div className="mx-auto flex min-h-screen w-full max-w-6xl flex-col px-6 py-8 md:px-10">
        <header className="flex items-start justify-between">
          <div className="relative mt-2 inline-block">
            <h1 className="away-logo-font text-4xl font-semibold tracking-tight sm:text-5xl">away.</h1>
            <span className="absolute -bottom-4 right-0 text-[10px] uppercase tracking-[0.25em] text-white/80">
              SANDBOX
            </span>
          </div>

          <nav aria-label="Primary" className="hidden sm:block">
            <ul className="flex gap-2 rounded-full border border-white/20 bg-white/10 p-1 backdrop-blur">
              {tabs.map((tab) => (
                <li key={tab}>
                  <button
                    type="button"
                    className="rounded-full px-4 py-1.5 text-sm font-medium text-white/85 transition hover:bg-white hover:text-[#1a262e]"
                  >
                    {tab}
                  </button>
                </li>
              ))}
            </ul>
          </nav>
        </header>

        <nav aria-label="Primary Mobile" className="mt-8 sm:hidden">
          <ul className="grid grid-cols-2 gap-2">
            {tabs.map((tab) => (
              <li key={tab}>
                <button
                  type="button"
                  className="w-full rounded-xl border border-white/20 bg-white/10 px-3 py-2 text-xs font-medium tracking-wide text-white/90"
                >
                  {tab}
                </button>
              </li>
            ))}
          </ul>
        </nav>

        <section className="flex flex-1 items-center justify-center">
          <div className="w-full max-w-2xl">
            <label htmlFor="instagram-link" className="mb-3 block text-center text-sm uppercase tracking-[0.22em] text-white/70">
              Paste Instagram Link
            </label>
            <form
              onSubmit={handleSubmit}
              className="group flex items-center gap-3 rounded-2xl border border-cyan-200/40 bg-white/8 px-4 py-3 shadow-[0_16px_35px_-20px_rgba(0,0,0,0.9),0_0_0_1px_rgba(255,255,255,0.08)_inset,0_0_24px_rgba(120,220,255,0.35)] transition focus-within:border-cyan-200/80 focus-within:shadow-[0_20px_45px_-20px_rgba(0,0,0,0.95),0_0_0_1px_rgba(255,255,255,0.14)_inset,0_0_32px_rgba(120,220,255,0.6)]"
            >
              <svg
                className="h-5 w-5 shrink-0 text-white/55"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.8"
                aria-hidden="true"
              >
                <circle cx="11" cy="11" r="7" />
                <path d="M20 20L17 17" />
              </svg>
              <input
                id="instagram-link"
                type="url"
                value={instagramUrl}
                onChange={(event) => setInstagramUrl(event.target.value)}
                placeholder="https://www.instagram.com/p/..."
                className="w-full bg-transparent text-base text-white placeholder:text-white/45 focus:outline-none"
              />
              <button
                type="submit"
                disabled={isSubmitting}
                className="rounded-xl border border-white/35 bg-white/14 px-4 py-2 text-sm font-medium text-white transition hover:bg-white hover:text-[#1a262e] disabled:opacity-70"
              >
                {isSubmitting ? "Sending..." : "Explore"}
              </button>
            </form>
            {statusMessage ? (
              <p className="mt-3 text-center text-sm text-white/75">{statusMessage}</p>
            ) : null}
          </div>
        </section>
      </div>
    </main>
  );
}
