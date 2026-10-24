"use client";

import { useEffect, useRef, useState } from "react";

const scenes = [
  { tag: "01 / THE CLAIM", claim: "Built a chat app using React and Node.", explanation: "It names the stack, but not your contribution.", level: "Listed", facts: ["React + Node", "Your contribution?", "What changed?"] },
  { tag: "02 / THE EVIDENCE", claim: "What part did you build yourself?", explanation: "The questions uncover details only you can supply.", level: "Evidence intake", facts: ["Built message search", "Deployed the app", "No measured result supplied"] },
  { tag: "03 / THE REWRITE", claim: "Built and deployed a React and Node chat app with message search.", explanation: "A stronger line, built only from the example facts beside it.", level: "Demonstrated", facts: ["React + Node", "Built message search", "Deployed the app"] }
];

export function ProofScene() {
  const [scene, setScene] = useState(0);
  const [autoplay, setAutoplay] = useState(true);
  const [started, setStarted] = useState(false);
  const sceneRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const reduce = () => window.matchMedia("(prefers-reduced-motion: reduce)").matches || document.documentElement.dataset.quiet === "true";
    if (reduce()) { setScene(2); setAutoplay(false); setStarted(true); }
    const observer = new IntersectionObserver(([entry]) => { if (entry.isIntersecting) { setStarted(true); observer.disconnect(); } }, { threshold: .15 });
    if (sceneRef.current) observer.observe(sceneRef.current);
    const onMotion = () => { if (reduce()) { setScene(2); setAutoplay(false); } };
    document.addEventListener("pramaan:motion", onMotion);
    return () => { observer.disconnect(); document.removeEventListener("pramaan:motion", onMotion); };
  }, []);
  useEffect(() => { if (!started || !autoplay || scene >= 2) return; const timer = window.setTimeout(() => setScene((value) => value + 1), 3400); return () => window.clearTimeout(timer); }, [started, autoplay, scene]);
  const current = scenes[scene];
  return <div className="proof-scene glass" ref={sceneRef} data-playing={autoplay && started && scene < 2}>
    <div className="scene-header"><span>PRAMAAN / PROOF IN MOTION</span><button type="button" onClick={() => { setScene(2); setAutoplay(false); }}>Skip animation <span aria-hidden="true">↗</span></button></div>
    <div className="scene-content"><div className="scene-claim"><span className="mono-label">ON THE RESUME</span><p key={scene}>{current.claim}</p><div className="scene-status"><span className="scene-spark" aria-hidden="true">✦</span><span>{current.level}</span><span className="scene-status-rule"/></div></div><div className="scene-evidence"><span className="mono-label">WHAT BACKS IT</span><ul>{current.facts.map((fact, index) => <li key={`${scene}-${fact}`}><span aria-hidden="true">{index === 0 || scene === 2 ? "✦" : "·"}</span>{fact}</li>)}</ul><p>{current.explanation}</p></div></div>
    <div className="scene-footer"><span>ILLUSTRATIVE EXAMPLE · NOT A REAL USER</span><div className="scene-steps" role="group" aria-label="Example stages">{scenes.map((item, index) => <button key={item.tag} type="button" onClick={() => { setScene(index); setAutoplay(false); }} className={scene === index ? "active" : ""} aria-pressed={scene === index}><span>0{index + 1}</span><span className="step-name">{["Claim", "Evidence", "Rewrite"][index]}</span></button>)}</div></div>
  </div>;
}

const claims = [
  { title: "Python", level: "Listed", detail: "It appears in a skills list. Add a project or experience to show where you used it.", kind: "listed" },
  { title: "API design", level: "Used", detail: "It appears in a project. Explain the problem and why you chose that approach.", kind: "used" },
  { title: "React app", level: "Demonstrated", detail: "A specific feature and your contribution show what you can defend in an interview.", kind: "demonstrated" },
  { title: "Measured result", level: "Quantified", detail: "A measured outcome you supplied, with its source kept beside the claim.", kind: "quantified" }
];

export function Constellation() {
  const [active, setActive] = useState(2);
  const chosen = claims[active];
  return <div className="constellation-experience glass"><div className="constellation-topline"><span>FIG. 01 / A PROFILE AS EVIDENCE</span><span>SELECT A CLAIM <span aria-hidden="true">↗</span></span></div><div className="constellation-canvas" role="group" aria-label="Example proof levels"><svg viewBox="0 0 840 380" preserveAspectRatio="none" aria-hidden="true"><path d="M95 258 265 122 505 230 727 82"/></svg>{claims.map((claim, index) => <button className={`constellation-point point-${index} ${claim.kind} ${active === index ? "active" : ""}`} key={claim.title} type="button" onClick={() => setActive(index)} aria-pressed={active === index}><span className="constellation-glyph" aria-hidden="true">✦</span><span>{claim.title}</span></button>)}</div><div className="constellation-description" aria-live="polite"><div><span className={`level-indicator ${chosen.kind}`} aria-hidden="true"/><span className="mono-label">{chosen.level}</span><h3>{chosen.title}</h3></div><p>{chosen.detail}</p></div><p className="scene-note">Illustrative map. Every proof level is explained in text.</p></div>;
}

export function MobileMenu() {
  const [open, setOpen] = useState(false);
  return <div className="mobile-menu"><button type="button" onClick={() => setOpen(!open)} aria-expanded={open} aria-controls="mobile-nav">{open ? "Close" : "Menu"}<span aria-hidden="true">{open ? "×" : "☰"}</span></button><nav id="mobile-nav" aria-label="Mobile" className={open ? "open" : ""}><a href="#idea" onClick={() => setOpen(false)}>The idea</a><a href="#proof" onClick={() => setOpen(false)}>See the proof</a><a href="#product" onClick={() => setOpen(false)}>The product</a></nav></div>;
}

export function MotionToggle() {
  const [quiet, setQuiet] = useState(false);
  useEffect(() => {
    const sync = () => setQuiet(document.documentElement.dataset.quiet === "true");
    sync();
    document.addEventListener("pramaan:motion", sync);
    return () => document.removeEventListener("pramaan:motion", sync);
  }, []);
  return <button className="motion-toggle" type="button" aria-pressed={quiet} onClick={() => { const next = !quiet; document.documentElement.dataset.quiet = String(next); document.dispatchEvent(new Event("pramaan:motion")); }}>{quiet ? "Play motion" : "Pause motion"}</button>;
}
