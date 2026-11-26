/*
 * bue-embed.js — renders BlueprintUE blueprints from local .txt files.
 *
 * Usage in a page (Markdown allows raw HTML):
 *   <div class="bue-embed" data-bp="anti-afk-kick" data-height="500px"></div>
 *
 * - data-bp:     blueprint id; loads docs/assets/blueprints/<id>.txt
 * - data-src:    (optional) explicit URL/path to a blueprint .txt instead of data-bp
 * - data-height: (optional) CSS height for the viewer, default 500px
 *
 * The renderer itself (window.blueprintUE.render.Main) comes from the vendored
 * bue-render/render.js. This loader only fetches the blueprint text and starts it.
 */
;(function () {
  "use strict";

  // Resolve this script's own URL, then the site root, so blueprint paths work
  // under any GitHub Pages sub-path and from pages at any depth.
  function selfSrc() {
    if (document.currentScript && document.currentScript.src) return document.currentScript.src;
    var s = document.querySelector('script[src*="bue-embed.js"]');
    return s ? s.src : null;
  }
  var SRC = selfSrc();
  // .../<site>/javascripts/bue-embed.js  ->  site root is one level up from javascripts/
  var SITE_ROOT = SRC ? new URL("../", SRC).href : "/";
  var BP_DIR = SITE_ROOT + "assets/blueprints/";

  function fail(target, id, url, err) {
    target.className = "bue-embed__error";
    target.innerHTML =
      "Could not render blueprint <code>" + id + "</code> (" +
      String((err && err.message) || err) + "). " +
      '<a href="' + url + '">Open the raw blueprint text</a>.';
  }

  function renderOne(el) {
    if (el.dataset.bueInit === "1") return;
    el.dataset.bueInit = "1";

    var id = el.getAttribute("data-bp") || "";
    var height = el.getAttribute("data-height") || "500px";
    var url = el.getAttribute("data-src")
      ? new URL(el.getAttribute("data-src"), SITE_ROOT).href
      : BP_DIR + id + ".txt";

    var target = document.createElement("div");
    el.appendChild(target);

    if (!id && !el.getAttribute("data-src")) {
      fail(target, "(none)", url, "missing data-bp");
      return;
    }

    fetch(url)
      .then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.text();
      })
      .then(function (text) {
        if (!(window.blueprintUE && window.blueprintUE.render && window.blueprintUE.render.Main)) {
          throw new Error("BlueprintUE renderer not loaded");
        }
        new window.blueprintUE.render.Main(text, target, { height: height }).start();
      })
      .catch(function (err) {
        fail(target, id || "(data-src)", url, err);
      });
  }

  // Render lazily: only when an embed scrolls near the viewport. The gallery
  // page can hold many heavy graphs, so this keeps initial load cheap.
  var io = ("IntersectionObserver" in window)
    ? new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) {
            io.unobserve(en.target);
            renderOne(en.target);
          }
        });
      }, { rootMargin: "300px 0px" })
    : null;

  function schedule(el) {
    if (el.dataset.bueInit === "1" || el.dataset.bueQueued === "1") return;
    if (io) {
      el.dataset.bueQueued = "1";
      io.observe(el);
    } else {
      renderOne(el);
    }
  }

  function renderAll() {
    var nodes = document.querySelectorAll(".bue-embed[data-bp], .bue-embed[data-src]");
    for (var i = 0; i < nodes.length; i++) schedule(nodes[i]);
  }

  // Material for MkDocs ships `document$` (fires on every page, incl. instant
  // navigation). Fall back to a normal load event otherwise.
  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(renderAll);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", renderAll);
  } else {
    renderAll();
  }
})();
