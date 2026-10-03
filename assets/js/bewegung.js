(() => {
  "use strict";

  const reduziert = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const kopfzeile = document.querySelector(".kopfzeile");
  if (kopfzeile) {
    const pruefen = () => {
      kopfzeile.classList.toggle("ist-gescrollt", window.scrollY > 8);
    };
    pruefen();
    window.addEventListener("scroll", pruefen, { passive: true });
  }

  if (reduziert) return;

  document.documentElement.classList.add("js-bewegung");

  function beobachten(elemente) {
    if (!("IntersectionObserver" in window)) {
      elemente.forEach((el) => el.classList.add("ist-sichtbar"));
      return;
    }

    const beobachter = new IntersectionObserver(
      (eintraege, obs) => {
        eintraege.forEach((eintrag) => {
          if (!eintrag.isIntersecting) return;
          eintrag.target.classList.add("ist-sichtbar");
          obs.unobserve(eintrag.target);
        });
      },
      { threshold: 0.12 }
    );

    elemente.forEach((el, i) => {
      el.style.transitionDelay = `${(i % 4) * 70}ms`;
      beobachter.observe(el);
    });
  }

  beobachten(Array.from(document.querySelectorAll(".einblenden, .freilegen")));

  document.addEventListener("raster:bereit", () => {
    beobachten(
      Array.from(
        document.querySelectorAll(
          ".einblenden:not(.ist-sichtbar), .freilegen:not(.ist-sichtbar)"
        )
      )
    );
  });

  function nachzuegler() {
    const hoehe = window.innerHeight || 0;
    document.querySelectorAll(".einblenden:not(.ist-sichtbar), .freilegen:not(.ist-sichtbar)")
      .forEach((el) => {
        const kasten = el.getBoundingClientRect();
        if (kasten.top < hoehe && kasten.bottom > 0) el.classList.add("ist-sichtbar");
      });
  }

  setTimeout(nachzuegler, 1200);
  let nachzueglerGeplant = false;
  window.addEventListener("scroll", () => {
    if (nachzueglerGeplant) return;
    nachzueglerGeplant = true;
    setTimeout(() => { nachzueglerGeplant = false; nachzuegler(); }, 250);
  }, { passive: true });
  window.addEventListener("load", () => setTimeout(nachzuegler, 400));

  function endzustandFestschreiben() {
    document.querySelectorAll(".ist-sichtbar:not(.ist-fertig)")
      .forEach((el) => el.classList.add("ist-fertig"));
  }

  setTimeout(endzustandFestschreiben, 2600);
  document.addEventListener("visibilitychange", () => {
    if (!document.hidden) {
      setTimeout(nachzuegler, 80);
      setTimeout(endzustandFestschreiben, 160);
    }
  });
  window.addEventListener("focus", () => setTimeout(endzustandFestschreiben, 160));

  function hochzaehlen(el) {
    const ziel = Number(el.dataset.zaehlziel);
    if (!Number.isFinite(ziel)) return;

    const dauer = 1100;
    const start = performance.now();
    let fertig = false;

    function schritt(jetzt) {
      const anteil = Math.min((jetzt - start) / dauer, 1);
      const weich = 1 - Math.pow(1 - anteil, 3);
      el.textContent = String(Math.round(ziel * weich));
      if (anteil < 1) {
        requestAnimationFrame(schritt);
      } else {
        fertig = true;
      }
    }

    el.textContent = "0";
    requestAnimationFrame(schritt);

    setTimeout(() => {
      if (!fertig) el.textContent = String(ziel);
    }, dauer + 700);
  }

  const zahlen = Array.from(document.querySelectorAll("[data-zaehlziel]"));
  if (zahlen.length) {
    if ("IntersectionObserver" in window) {
      const zaehlBeobachter = new IntersectionObserver(
        (eintraege, obs) => {
          eintraege.forEach((eintrag) => {
            if (!eintrag.isIntersecting) return;
            obs.unobserve(eintrag.target);
            hochzaehlen(eintrag.target);
          });
        },
        { threshold: 0.6 }
      );
      zahlen.forEach((el) => zaehlBeobachter.observe(el));
    } else {
      zahlen.forEach(hochzaehlen);
    }
  }

  const folge = document.querySelector(".folge");
  if (folge) {
    const strich = folge.querySelector(".folge__strich");
    let bilder = [];
    let schritte = [];
    let letzterIndex = -1;

    function folgeEinsammeln() {
      bilder = Array.from(folge.querySelectorAll(".folge__bild > *"));
      schritte = Array.from(folge.querySelectorAll(".folge__schritt"));
      letzterIndex = -1;
    }

    function folgeAktualisieren() {
      if (bilder.length < 2) return;

      const kasten = folge.getBoundingClientRect();

      const sichtHoehe =
        window.innerHeight || document.documentElement.clientHeight || 1;
      const strecke = Math.max(kasten.height - sichtHoehe, 1);
      const anteil = Math.min(Math.max(-kasten.top / strecke, 0), 1);

      if (strich) strich.style.setProperty("--anteil", anteil.toFixed(4));

      const index = Math.round(anteil * (bilder.length - 1));
      if (index === letzterIndex) return;
      letzterIndex = index;

      bilder.forEach((bild, i) => bild.classList.toggle("ist-dran", i === index));
      schritte.forEach((s, i) => s.classList.toggle("ist-dran", i === index));
    }

    folgeEinsammeln();
    window.addEventListener("scroll", folgeAktualisieren, { passive: true });
    window.addEventListener("resize", folgeAktualisieren, { passive: true });

    document.addEventListener("raster:bereit", () => {
      folgeEinsammeln();
      folgeAktualisieren();
    });

    folgeAktualisieren();
  }

  const heroband = document.querySelector(".heroband");
  if (heroband) {
    function versatzSetzen() {
      const kasten = heroband.getBoundingClientRect();
      const hoehe = window.innerHeight || document.documentElement.clientHeight || 1;
      if (kasten.bottom < 0 || kasten.top > hoehe) return;

      const mitte = kasten.top + kasten.height / 2;
      const lage = (mitte - hoehe / 2) / (hoehe / 2 + kasten.height / 2);
      const weg = Math.max(-1, Math.min(1, lage)) * (kasten.height * 0.06);
      heroband.style.setProperty("--versatz", `${weg.toFixed(1)}px`);
    }

    window.addEventListener("scroll", versatzSetzen, { passive: true });
    window.addEventListener("resize", versatzSetzen, { passive: true });
    window.addEventListener("load", versatzSetzen);
    versatzSetzen();
  }
})();
