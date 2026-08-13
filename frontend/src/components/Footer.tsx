const year = new Date().getFullYear();

export function Footer() {
  return (
    <footer className="mt-10 bg-night-800 pb-7 pt-14 text-white/85">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <div className="grid grid-cols-1 gap-8 border-b border-white/10 pb-9 sm:grid-cols-2 lg:grid-cols-[1.4fr_1fr_1fr_1fr]">
          <div>
            <a href="#top" className="flex items-center gap-2 text-lg font-semibold text-white">
              <span className="text-radar-400">📡</span>Voa Radar
            </a>
            <p className="mt-3.5 max-w-[260px] text-sm leading-relaxed text-white/60">
              Encontre as melhores passagens aéreas em segundos — feito pela RhoneyInc.
            </p>
            <span className="mt-4 inline-block rounded-lg bg-radar-500/15 px-3 py-1.5 font-mono text-xs tracking-wide text-radar-400">
              Uma conta. Todos os softwares.
            </span>
            <div className="mt-4 flex gap-2.5">
              <a
                href="https://github.com/RonaldoRhoney"
                target="_blank"
                rel="noopener"
                aria-label="GitHub"
                className="grid h-[34px] w-[34px] place-items-center rounded-full bg-white/8 text-sm"
              >
                💻
              </a>
              <a
                href="https://www.instagram.com/ronaldorhoney"
                target="_blank"
                rel="noopener"
                aria-label="Instagram"
                className="grid h-[34px] w-[34px] place-items-center rounded-full bg-white/8 text-sm"
              >
                📷
              </a>
              <a
                href="https://www.linkedin.com/in/ronaldomartinsrhoney/"
                target="_blank"
                rel="noopener"
                aria-label="LinkedIn"
                className="grid h-[34px] w-[34px] place-items-center rounded-full bg-white/8 text-sm"
              >
                💼
              </a>
            </div>
          </div>

          <div>
            <h5 className="mb-3.5 font-mono text-xs uppercase tracking-wider text-radar-400">Produto</h5>
            <a href="/" className="mb-2.5 block text-sm text-white/75 hover:text-white">Buscar viagens</a>
          </div>

          <div>
            <h5 className="mb-3.5 font-mono text-xs uppercase tracking-wider text-radar-400">RhoneyInc</h5>
            <a href="https://rhoneyinc.com" className="mb-2.5 block text-sm text-white/75 hover:text-white">Sobre nós</a>
            <a href="https://meupet.rhoneyinc.com" className="mb-2.5 block text-sm text-white/75 hover:text-white">MeuPet</a>
            <a href="https://menuflex.rhoneyinc.com" className="mb-2.5 block text-sm text-white/75 hover:text-white">MenuFlex</a>
            <a href="https://fitnow.rhoneyinc.com" className="mb-2.5 block text-sm text-white/75 hover:text-white">FitNow</a>
          </div>

          <div>
            <h5 className="mb-3.5 font-mono text-xs uppercase tracking-wider text-radar-400">Legal</h5>
            <a href="/privacidade.html" className="mb-2.5 block text-sm text-white/75 hover:text-white">Privacidade (LGPD)</a>
            <a href="/termos.html" className="mb-2.5 block text-sm text-white/75 hover:text-white">Termos de uso</a>
            <a href="/contato.html" className="mb-2.5 block text-sm text-white/75 hover:text-white">Contato</a>
          </div>
        </div>

        <div className="flex flex-wrap items-center justify-between gap-3 pt-[22px] text-xs text-white/55">
          <span>© {year} Voa Radar — um produto RhoneyInc. Todos os direitos reservados.</span>
          <span className="font-mono">voaradar.rhoneyinc.com</span>
        </div>
      </div>
    </footer>
  );
}
