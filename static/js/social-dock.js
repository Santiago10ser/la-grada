(function() {
  const style = document.createElement('style');
  style.textContent = `
    .social-dock {
      position: fixed;
      bottom: 1.5rem;
      right: 1.5rem;
      z-index: 9999;
      display: flex;
      flex-direction: column-reverse;
      align-items: flex-end;
      gap: 0.7rem;
      font-family: 'Barlow', sans-serif;
    }
    .social-dock-links {
      display: flex;
      flex-direction: column-reverse;
      gap: 0.7rem;
      opacity: 0;
      transform: translateY(12px);
      pointer-events: none;
      transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }
    .social-dock.open .social-dock-links {
      opacity: 1;
      transform: translateY(0);
      pointer-events: all;
    }
    .social-dock-item {
      width: 50px;
      height: 50px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      text-decoration: none;
      box-shadow: 0 4px 16px rgba(0,0,0,0.4);
      transition: transform 0.2s;
      position: relative;
    }
    .social-dock-item:hover { transform: scale(1.1); }
    .social-dock-item svg { width: 22px; height: 22px; }
    .social-dock-ig { background: linear-gradient(135deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888); }
    .social-dock-tk { background: #111; border: 1px solid rgba(201,168,76,0.4); }

    .social-dock-tooltip {
      position: absolute;
      right: 60px;
      top: 50%;
      transform: translateY(-50%);
      background: #0a0a0a;
      color: #f5f2ec;
      font-size: 0.7rem;
      letter-spacing: 0.05em;
      padding: 5px 10px;
      border: 1px solid rgba(201,168,76,0.3);
      white-space: nowrap;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.2s;
    }
    .social-dock-item:hover .social-dock-tooltip { opacity: 1; }

    .social-dock-toggle {
      width: 58px;
      height: 58px;
      border-radius: 50%;
      background: #c9a84c;
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 6px 20px rgba(0,0,0,0.5);
      transition: transform 0.2s, background 0.2s;
    }
    .social-dock-toggle:hover { background: #e8c97a; transform: scale(1.05); }
    .social-dock-toggle svg { width: 24px; height: 24px; color: #000; transition: transform 0.3s; }
    .social-dock.open .social-dock-toggle svg.icon-share { display: none; }
    .social-dock:not(.open) .social-dock-toggle svg.icon-close { display: none; }

    @media (max-width: 480px) {
      .social-dock { bottom: 1rem; right: 1rem; }
      .social-dock-toggle { width: 52px; height: 52px; }
      .social-dock-item { width: 46px; height: 46px; }
    }
  `;
  document.head.appendChild(style);

  const dock = document.createElement('div');
  dock.className = 'social-dock';
  dock.innerHTML = `
    <button class="social-dock-toggle" id="socialDockToggle" aria-label="Redes sociales">
      <svg class="icon-share" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
      <svg class="icon-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
    </button>
    <div class="social-dock-links">
      <a href="https://instagram.com/lagradapy" target="_blank" rel="noreferrer" class="social-dock-item social-dock-ig" aria-label="Instagram">
        <span class="social-dock-tooltip">@lagradapy</span>
        <svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="white" stroke="none"/></svg>
      </a>
      <a href="https://tiktok.com/@lagradapy" target="_blank" rel="noreferrer" class="social-dock-item social-dock-tk" aria-label="TikTok">
        <span class="social-dock-tooltip">@lagradapy</span>
        <svg viewBox="0 0 24 24" fill="#c9a84c"><path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-2.88 2.5 2.89 2.89 0 01-2.89-2.89 2.89 2.89 0 012.89-2.89c.28 0 .54.04.79.1V9.01a6.33 6.33 0 00-.79-.05 6.34 6.34 0 00-6.34 6.34 6.34 6.34 0 006.34 6.34 6.34 6.34 0 006.33-6.34V8.69a8.18 8.18 0 004.78 1.52V6.76a4.85 4.85 0 01-1.01-.07z"/></svg>
      </a>
    </div>
  `;
  document.body.appendChild(dock);

  document.getElementById('socialDockToggle').addEventListener('click', () => {
    dock.classList.toggle('open');
  });

  document.addEventListener('click', (e) => {
    if (!dock.contains(e.target)) dock.classList.remove('open');
  });
})();
