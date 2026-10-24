"use client";

import { useEffect, useRef, useState, type ReactNode } from "react";

type Speck = { angle: number; radius: number; depth: number; size: number; phase: number; orbit: number };

export function FloatingHeader({ children }: { children: ReactNode }) {
  const [scrolled, setScrolled] = useState(false);
  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 48);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);
  return <header className={`site-header${scrolled ? " is-scrolled" : ""}`}><div className="header-inner">{children}</div></header>;
}

export function CinematicField() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const context = canvas?.getContext("2d", { alpha: true });
    if (!canvas || !context) return;

    const motionPreference = window.matchMedia("(prefers-reduced-motion: reduce)");
    const saveData = !!(navigator as Navigator & { connection?: { saveData?: boolean } }).connection?.saveData;
    const random = (seed: number) => { const value = Math.sin(seed * 79.71) * 43758.5453; return value - Math.floor(value); };
    let width = 0;
    let height = 0;
    let specks: Speck[] = [];
    let frame = 0;
    let start = 0;
    let raf = 0;
    let inView = true;
    let reduced = motionPreference.matches || document.documentElement.dataset.quiet === "true" || saveData;

    const draw = (time: number) => {
      context.clearRect(0, 0, width, height);
      const progress = reduced ? 1 : Math.min(1, time / 4400);
      const reveal = .28 + .72 * (1 - Math.pow(1 - progress, 3));
      const centerX = width * (width < 640 ? .58 : .76);
      const centerY = height * (width < 640 ? .36 : .46);
      const size = Math.min(width * (width < 640 ? .68 : .38), height * .55);

      // Layered, slow moving haze creates depth without a large video asset.
      for (let i = 0; i < 9; i++) {
        const angle = i * 2.399 + time * .000025;
        const x = centerX + Math.cos(angle) * size * (.16 + i * .04);
        const y = centerY + Math.sin(angle) * size * (.13 + i * .025);
        const radius = size * (.46 + random(i + 91) * .3);
        const cloud = context.createRadialGradient(x, y, 0, x, y, radius);
        cloud.addColorStop(0, i % 3 === 0 ? `rgba(165,112,73,${.075 * reveal})` : `rgba(137,122,105,${.075 * reveal})`);
        cloud.addColorStop(.55, `rgba(81,71,63,${.052 * reveal})`);
        cloud.addColorStop(1, "rgba(12,11,10,0)");
        context.fillStyle = cloud;
        context.fillRect(x - radius, y - radius, radius * 2, radius * 2);
      }

      context.save();
      context.translate(centerX, centerY);
      context.rotate(-.28 + time * .000015);
      context.scale(1, .63);
      context.beginPath();
      context.ellipse(0, 0, size * .82, size * .82, 0, .08, Math.PI * 1.64);
      context.strokeStyle = `rgba(230,204,166,${.16 * reveal})`;
      context.lineWidth = 1.1;
      context.stroke();
      context.restore();

      for (let i = 0; i < specks.length; i++) {
        const speck = specks[i];
        const angle = speck.angle + time * .000047 * speck.orbit;
        const radius = size * (.13 + speck.radius * 1.08);
        const scatter = .55 + reveal * .45;
        const x = centerX + Math.cos(angle) * radius * scatter;
        const y = centerY + Math.sin(angle) * radius * .68 * scatter + Math.sin(angle * 3 + speck.phase) * size * .08;
        const shimmer = reduced ? 1 : .8 + .2 * Math.sin(time * .0014 + speck.phase);
        const alpha = (.17 + speck.depth * .72) * reveal * shimmer;
        context.beginPath();
        context.arc(x, y, speck.size * (.55 + speck.depth * .5), 0, Math.PI * 2);
        context.fillStyle = i % 11 === 0 ? `rgba(245,188,121,${alpha})` : `rgba(239,230,215,${alpha})`;
        context.fill();
        if (!reduced && progress < .8 && i % 7 === 0) {
          context.beginPath();
          context.moveTo(x, y);
          context.lineTo(x + Math.cos(angle) * (1 - progress) * 34, y + Math.sin(angle) * (1 - progress) * 20);
          context.strokeStyle = `rgba(234,216,189,${(1 - progress) * .3})`;
          context.lineWidth = .7;
          context.stroke();
        }
      }

      const core = context.createRadialGradient(centerX, centerY, 0, centerX, centerY, size * .35);
      core.addColorStop(0, `rgba(251,225,181,${.22 * reveal})`);
      core.addColorStop(.3, `rgba(180,118,73,${.07 * reveal})`);
      core.addColorStop(1, "rgba(15,11,9,0)");
      context.fillStyle = core;
      context.fillRect(centerX - size * .35, centerY - size * .35, size * .7, size * .7);
    };

    const resize = () => {
      const rect = canvas.getBoundingClientRect();
      width = rect.width;
      height = rect.height;
      const ratio = Math.min(window.devicePixelRatio || 1, 1.5);
      canvas.width = Math.round(width * ratio);
      canvas.height = Math.round(height * ratio);
      context.setTransform(ratio, 0, 0, ratio, 0, 0);
      specks = Array.from({ length: width < 640 ? 310 : 820 }, (_, index) => ({
        angle: random(index + 12) * Math.PI * 2,
        radius: Math.sqrt(random(index + 41)),
        depth: random(index + 101),
        size: .35 + random(index + 331) * 1.65,
        phase: random(index + 444) * Math.PI * 2,
        orbit: .65 + random(index + 555) * .9
      }));
      draw(reduced ? 4400 : frame);
    };

    const animate = (timestamp: number) => {
      if (!inView || document.hidden || reduced) return;
      if (!start) start = timestamp;
      frame = timestamp - start;
      draw(frame);
      raf = requestAnimationFrame(animate);
    };
    const resume = () => {
      cancelAnimationFrame(raf);
      if (inView && !document.hidden && !reduced) raf = requestAnimationFrame(animate);
    };
    const onMotion = () => {
      reduced = motionPreference.matches || document.documentElement.dataset.quiet === "true" || saveData;
      draw(reduced ? 4400 : frame);
      resume();
    };
    const observer = new IntersectionObserver(([entry]) => { inView = entry.isIntersecting; resume(); }, { threshold: .01 });
    const sizeObserver = new ResizeObserver(resize);
    sizeObserver.observe(canvas);
    observer.observe(canvas);
    document.addEventListener("visibilitychange", resume);
    document.addEventListener("pramaan:motion", onMotion);
    motionPreference.addEventListener("change", onMotion);
    resize();
    resume();
    return () => {
      cancelAnimationFrame(raf);
      sizeObserver.disconnect();
      observer.disconnect();
      document.removeEventListener("visibilitychange", resume);
      document.removeEventListener("pramaan:motion", onMotion);
      motionPreference.removeEventListener("change", onMotion);
    };
  }, []);

  return <canvas ref={canvasRef} className="particle-field" aria-hidden="true"/>;
}
