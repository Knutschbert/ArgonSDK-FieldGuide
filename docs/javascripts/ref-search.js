/*
 * ref-search.js — a second, independent search box for the C++/BP reference.
 *
 * Drop this anywhere in a page:
 *   <div class="ref-search" data-placeholder="Search C++/BP reference…"></div>
 *
 * It lazy-loads docs/assets/reference-inventory.json (the same file the
 * [[ref:...]] link hook uses) and searches the reference symbols client-side,
 * ranking by substring so e.g. "TBLPlayerController" surfaces
 * "ATBLPlayerController". Results link out to the published reference site.
 *
 * This is deliberately separate from the Field Guide's own Material search:
 * two boxes, two independent datasets.
 */
;(function () {
  "use strict";

  function selfSrc() {
    if (document.currentScript && document.currentScript.src) return document.currentScript.src;
    var s = document.querySelector('script[src*="ref-search.js"]');
    return s ? s.src : null;
  }
  var SRC = selfSrc();
  var SITE_ROOT = SRC ? new URL("../", SRC).href : "/";

  var MAX_RESULTS = 40;
  var _data = null;      // {entries:[{name,url,kind}], ...}
  var _loading = null;   // in-flight promise

  function loadInventory(url) {
    if (_data) return Promise.resolve(_data);
    if (_loading) return _loading;
    _loading = fetch(url)
      .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
      .then(function (json) { _data = json; return json; });
    return _loading;
  }

  // Score a candidate name against a lowercased query. Lower is better; -1 = no match.
  function score(nameLower, q) {
    if (nameLower === q) return 0;
    var idx = nameLower.indexOf(q);
    if (idx === -1) return -1;
    if (idx === 0) return 1 + nameLower.length / 1000;      // prefix match
    // prefer matches at an internal word/camel boundary
    var prev = nameLower.charAt(idx - 1);
    var boundary = /[^a-z0-9]/.test(prev);
    return (boundary ? 2 : 3) + nameLower.length / 1000;
  }

  function search(entries, query) {
    var q = query.trim().toLowerCase();
    if (q.length < 2) return [];
    var scored = [];
    for (var i = 0; i < entries.length; i++) {
      var s = score(entries[i].name.toLowerCase(), q);
      if (s >= 0) scored.push([s, entries[i]]);
    }
    scored.sort(function (a, b) {
      if (a[0] !== b[0]) return a[0] - b[0];
      return a[1].name.localeCompare(b[1].name);
    });
    return scored.slice(0, MAX_RESULTS).map(function (x) { return x[1]; });
  }

  function build(el) {
    if (el.dataset.refInit === "1") return;
    el.dataset.refInit = "1";

    var invUrl = el.getAttribute("data-inventory") || (SITE_ROOT + "assets/reference-search.json");
    var placeholder = el.getAttribute("data-placeholder") || "Search C++/BP reference…";

    var input = document.createElement("input");
    input.type = "search";
    input.className = "ref-search__input";
    input.setAttribute("placeholder", placeholder);
    input.setAttribute("autocomplete", "off");
    input.setAttribute("spellcheck", "false");
    input.setAttribute("aria-label", placeholder);

    var status = document.createElement("div");
    status.className = "ref-search__status";

    var list = document.createElement("ul");
    list.className = "ref-search__results";

    el.appendChild(input);
    el.appendChild(status);
    el.appendChild(list);

    var active = -1;
    var current = [];

    function render(results) {
      current = results;
      active = -1;
      list.innerHTML = "";
      results.forEach(function (e, i) {
        var li = document.createElement("li");
        var a = document.createElement("a");
        a.href = e.url;
        a.className = "ref-search__hit";
        a.dataset.i = i;
        var kind = (e.kind && e.kind !== "page") ? e.kind : "";
        a.innerHTML = (kind ? '<span class="ref-search__kind">' + kind + "</span>" : "") +
                      '<span class="ref-search__name"></span>';
        a.querySelector(".ref-search__name").textContent = e.name;
        li.appendChild(a);
        list.appendChild(li);
      });
    }

    function run() {
      var q = input.value;
      if (q.trim().length < 2) { list.innerHTML = ""; status.textContent = ""; return; }
      status.textContent = "Loading reference index…";
      loadInventory(invUrl).then(function (data) {
        var results = search(data.entries || [], q);
        status.textContent = results.length
          ? (results.length >= MAX_RESULTS ? "Showing first " + MAX_RESULTS + " matches" : results.length + " match" + (results.length === 1 ? "" : "es"))
          : "No matches in " + (data.count || "the") + " reference pages";
        render(results);
      }).catch(function (err) {
        status.textContent = "Could not load the reference index (" + (err.message || err) + ").";
      });
    }

    var t;
    input.addEventListener("input", function () { clearTimeout(t); t = setTimeout(run, 120); });

    input.addEventListener("keydown", function (ev) {
      var items = list.querySelectorAll(".ref-search__hit");
      if (ev.key === "ArrowDown" || ev.key === "ArrowUp") {
        ev.preventDefault();
        if (!items.length) return;
        active += (ev.key === "ArrowDown") ? 1 : -1;
        if (active < 0) active = items.length - 1;
        if (active >= items.length) active = 0;
        items.forEach(function (n) { n.classList.remove("is-active"); });
        items[active].classList.add("is-active");
        items[active].scrollIntoView({ block: "nearest" });
      } else if (ev.key === "Enter") {
        if (active >= 0 && items[active]) { ev.preventDefault(); window.location.href = items[active].href; }
        else if (items.length) { ev.preventDefault(); window.location.href = items[0].href; }
      } else if (ev.key === "Escape") {
        input.value = ""; list.innerHTML = ""; status.textContent = "";
      }
    });
  }

  function buildAll() {
    var nodes = document.querySelectorAll(".ref-search");
    for (var i = 0; i < nodes.length; i++) build(nodes[i]);
  }

  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(buildAll);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", buildAll);
  } else {
    buildAll();
  }
})();
