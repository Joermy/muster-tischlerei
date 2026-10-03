(() => {
  "use strict";

  const WURZEL = document.body.dataset.wurzel || "";

  const sicher = (wert) => {
    const div = document.createElement("div");
    div.textContent = wert == null ? "" : String(wert);
    return div.innerHTML;
  };

  function bild(name, optionen) {
    const b = (window.BILDER || {})[name];
    if (!b) return "";
    const o = optionen || {};
    const srcset = b.breiten
      .map((w) => `${WURZEL}bilder/${name}-${w}.webp ${w}w`)
      .join(", ");
    const gross = b.breiten[b.breiten.length - 1];
    const eifrig = o.eifrig === true;
    return (
      `<img src="${WURZEL}bilder/${name}-${gross}.webp"` +
      ` srcset="${srcset}"` +
      ` sizes="${o.sizes || "100vw"}"` +
      ` width="${b.breite}" height="${b.hoehe}"` +
      ` alt="${sicher(o.alt != null ? o.alt : b.alt)}"` +
      (eifrig
        ? ' fetchpriority="high" decoding="async"'
        : ' loading="lazy" decoding="async"') +
      ">"
    );
  }

  function rahmen(name, klasse, optionen) {
    const b = (window.BILDER || {})[name];
    if (!b) return "";
    const stil = `--platzhalter:${b.farbe}`;
    return (
      `<div class="bild ${klasse}" style="${stil}">` +
      bild(name, optionen) +
      "</div>"
    );
  }

  window.BILDBAU = { bild, rahmen };

  document.querySelectorAll(".klapp__knopf").forEach((knopf) => {
    const inhalt = document.getElementById(knopf.getAttribute("aria-controls"));
    if (!inhalt) return;

    knopf.addEventListener("click", () => {
      const offen = knopf.getAttribute("aria-expanded") === "true";

      if (offen) {
        inhalt.style.height = `${inhalt.scrollHeight}px`;
        requestAnimationFrame(() => {
          inhalt.style.height = "0px";
        });
        knopf.setAttribute("aria-expanded", "false");
      } else {
        inhalt.style.height = `${inhalt.scrollHeight}px`;
        knopf.setAttribute("aria-expanded", "true");

        inhalt.addEventListener(
          "transitionend",
          () => {
            if (knopf.getAttribute("aria-expanded") === "true") {
              inhalt.style.height = "auto";
            }
          },
          { once: true }
        );
      }
    });
  });

  let etwasGebaut = false;

  const raster = document.getElementById("leistungen-raster");
  if (raster && Array.isArray(window.LEISTUNGEN)) {
    raster.innerHTML = window.LEISTUNGEN.map((leistung, i) => {
      const nummer = String(i + 1).padStart(2, "0");
      const foto = leistung.bild
        ? `<div class="leistung__bild">` +
          `<p class="leistung__nummer">${nummer}</p>` +
          rahmen(leistung.bild, "bild--3-2", {
            sizes: "(max-width: 640px) 90vw, (max-width: 1100px) 45vw, 520px",
          }) +
          "</div>"
        : `<p class="leistung__nummer">${nummer}</p>`;
      return (
        '<article class="leistung einblenden">' +
        foto +
        `<h3>${sicher(leistung.titel)}</h3>` +
        `<p>${sicher(leistung.text)}</p>` +
        "</article>"
      );
    }).join("");
    etwasGebaut = true;
  }

  const projektraster = document.getElementById("projekte-raster");
  if (projektraster && Array.isArray(window.PROJEKTE)) {
    projektraster.innerHTML = window.PROJEKTE.map(
      (p) =>
        '<article class="projekt einblenden">' +
        '<div class="freilegen">' +
        rahmen(p.bild, "bild--4-3", {
          sizes: "(max-width: 640px) 90vw, (max-width: 1100px) 45vw, 600px",
        }) +
        "</div>" +
        '<div class="projekt__zeile">' +
        `<span class="projekt__titel">${sicher(p.titel)}</span>` +
        `<span class="projekt__meta">${sicher(p.material)} · ${sicher(
          p.ort
        )} ${sicher(p.jahr)}</span>` +
        "</div>" +
        "</article>"
    ).join("");
    etwasGebaut = true;
  }

  const folge = document.getElementById("folge-bilder");
  if (folge && Array.isArray(window.FOLGE)) {
    folge.innerHTML = window.FOLGE.map(
      (f, i) =>
        `<div${i === 0 ? ' class="ist-dran"' : ""}>` +
        bild(f.bild, { sizes: "(max-width: 760px) 90vw, min(86vmin, 980px)" }) +
        "</div>"
    ).join("");

    const liste = document.getElementById("folge-schritte");
    if (liste) {
      liste.innerHTML = window.FOLGE.map(
        (f, i) =>
          `<li class="folge__schritt${i === 0 ? " ist-dran" : ""}">` +
          `${String(i + 1).padStart(2, "0")} &nbsp; ${sicher(f.schritt)}</li>`
      ).join("");
    }
    etwasGebaut = true;
  }

  const muster = document.getElementById("holz-muster");
  if (muster && Array.isArray(window.HOELZER)) {
    muster.innerHTML = window.HOELZER.map(
      (h) =>
        '<div class="muster__feld" tabindex="0">' +
        bild(h.bild, { sizes: "(max-width: 640px) 45vw, 240px" }) +
        `<span class="muster__name">${sicher(h.name)}</span>` +
        "</div>"
    ).join("");
    etwasGebaut = true;
  }

  if (etwasGebaut) {
    document.dispatchEvent(new CustomEvent("raster:bereit"));
  }
})();
