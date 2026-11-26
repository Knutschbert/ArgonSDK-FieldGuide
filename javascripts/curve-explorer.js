(() => {
  const examples = {
    slash: {
      name: "Slash cooldown",
      unit: "seconds",
      max: 5,
      m: 1, k: 3, c: 0, b: 0, type: "Polynomial",
      description: "BC_Slash_C uses I_TimeSinceLastAttack to make Slash more attractive as time passes.",
      interpretation: "Immediately after an attack, this consideration contributes little. Its influence rises increasingly quickly toward the configured range maximum."
    },
    overhead: {
      name: "Overhead/Stab cooldown",
      unit: "seconds",
      max: 1,
      m: 1, k: 3, c: 0, b: 0, type: "Polynomial",
      description: "BC_OverheadStab_C uses I_TimeSinceLastAttack with a shorter configured range.",
      interpretation: "This has the same curve family as Slash cooldown but reaches its configured maximum after less elapsed time."
    },
    blockDistance: {
      name: "Block distance",
      unit: "game units",
      max: 375,
      m: -1, k: 10, c: 0, b: 1, type: "Polynomial",
      description: "BC_Block_C uses I_Distance to strongly prefer defensive behavior at close range.",
      interpretation: "The score remains high near the target and falls only when distance becomes large relative to this behavior's range."
    },
    blockRepeat: {
      name: "Block repeat timing",
      unit: "seconds",
      max: 6,
      m: 10, k: 1, c: 0.85, b: 0, type: "Linear",
      description: "BC_Block_C uses I_TimeSinceLastDidBehavior to avoid repeating block too quickly.",
      interpretation: "After clamping, the score is near zero until the normalized input reaches the configured center, then it rises very quickly."
    },
    wait: {
      name: "Wait fallback",
      unit: "normalized",
      max: 1,
      m: 0, k: 1, c: 0, b: 0.25, type: "Linear",
      description: "BC_Wait_C uses a constant consideration as a low fallback.",
      interpretation: "The curve stays at a fixed low score. It gives Wait a stable fallback role rather than responding to world change."
    },
    shove: {
      name: "Shove: recent enemy blocks",
      unit: "recent blocks",
      max: 4,
      m: 1, k: 2, c: 0, b: 0, type: "Polynomial",
      description: "BC_Shove_C uses I_TimesEnemyRecentlyBlockedMe as one influence on shove pressure.",
      interpretation: "The score grows more strongly as recent blocks accumulate, but it is still only one influence on Shove."
    },
    feint: {
      name: "Feint randomness",
      unit: "random value",
      max: 1,
      m: 1, k: 1, c: 0, b: 0, type: "Linear",
      description: "BC_FeintAttack_C uses I_Random to reduce the frequency of feint consideration.",
      interpretation: "Higher random samples contribute a higher score; this is not a direct published feint probability."
    }
  };

  const clamp = (value) => Math.max(0, Math.min(1, Number.isFinite(value) ? value : 0));
  const curve = (x, e) => {
    const offset = x - e.c;
    let value;
    switch (e.type) {
      case "Linear": value = e.m * offset + e.b; break;
      case "Polynomial": value = e.m * Math.pow(offset, e.k) + e.b; break;
      case "Logistic": value = e.m / (Math.exp(-10 * e.k * (offset - 0.5)) + 1) + e.b; break;
      case "Logit": value = Math.log(offset / (1 - offset)) * e.m * 0.2 + 0.5 + e.b; break;
      case "Normal": value = e.m * Math.exp(-30 * e.k * Math.pow(offset - 0.5, 2)) + e.b; break;
      case "Sine": value = (Math.sin(offset * 2 * Math.PI) * e.m + 1) * 0.5 + e.b; break;
      default: value = 0;
    }
    return clamp(value);
  };

  function draw(svg, e, current) {
    const ns = "http://www.w3.org/2000/svg";
    const make = (tag, attributes, text) => {
      const node = document.createElementNS(ns, tag);
      Object.entries(attributes || {}).forEach(([key, value]) => node.setAttribute(key, value));
      if (text) node.textContent = text;
      return node;
    };
    svg.replaceChildren();
    const left = 65, top = 25, width = 610, height = 260, bottom = top + height;
    const x = (value) => left + value * width;
    const y = (value) => bottom - value * height;

    svg.append(make("rect", { x: left, y: top, width, height, fill: "none", stroke: "currentColor", "stroke-width": 1 }));
    for (let i = 0; i <= 4; i += 1) {
      const value = i / 4;
      svg.append(make("line", { x1: x(value), y1: top, x2: x(value), y2: bottom, stroke: "currentColor", "stroke-opacity": 0.16 }));
      svg.append(make("line", { x1: left, y1: y(value), x2: left + width, y2: y(value), stroke: "currentColor", "stroke-opacity": 0.16 }));
      svg.append(make("text", { x: x(value), y: bottom + 24, "text-anchor": "middle", "font-size": 14 }, value.toFixed(2)));
      svg.append(make("text", { x: left - 10, y: y(value) + 5, "text-anchor": "end", "font-size": 14 }, value.toFixed(2)));
    }
    let points = "";
    for (let i = 0; i <= 160; i += 1) {
      const value = i / 160;
      points += `${x(value)},${y(curve(value, e))} `;
    }
    svg.append(make("polyline", { points, fill: "none", stroke: "#ffb300", "stroke-width": 3 }));
    const score = curve(current, e);
    svg.append(make("line", { x1: x(current), y1: bottom, x2: x(current), y2: y(score), stroke: "#4fc3f7", "stroke-width": 2, "stroke-dasharray": "5 4" }));
    svg.append(make("circle", { cx: x(current), cy: y(score), r: 6, fill: "#4fc3f7" }));
    svg.append(make("text", { x: left + width / 2, y: 345, "text-anchor": "middle", "font-size": 16 }, "Normalized input"));
    svg.append(make("text", { x: 18, y: top + height / 2, transform: `rotate(-90 18 ${top + height / 2})`, "text-anchor": "middle", "font-size": 16 }, "Curve score"));
  }

  function init(root) {
    const select = root.querySelector("[data-curve-example]");
    const slider = root.querySelector("[data-curve-input]");
    const svg = root.querySelector("[data-curve-plot]");
    const output = root.querySelector("[data-curve-normalized]");
    Object.entries(examples).forEach(([key, example]) => select.add(new Option(example.name, key)));

    const render = () => {
      const e = examples[select.value];
      const normalized = Number(slider.value);
      const score = curve(normalized, e);
      root.querySelector("[data-curve-description]").textContent = e.description;
      output.value = normalized.toFixed(2);
      root.querySelector("[data-curve-raw]").textContent = `${(normalized * e.max).toFixed(2)} ${e.unit}`;
      root.querySelector("[data-curve-range]").textContent = `0–${e.max} ${e.unit}`;
      root.querySelector("[data-curve-parameters]").textContent = `${e.type}; M=${e.m}, K=${e.k}, C=${e.c}, B=${e.b}`;
      root.querySelector("[data-curve-score]").textContent = score.toFixed(3);
      root.querySelector("[data-curve-interpretation]").textContent = e.interpretation;
      draw(svg, e, normalized);
    };
    select.addEventListener("change", render);
    slider.addEventListener("input", render);
    render();
  }

  const start = () => document.querySelectorAll("[data-curve-explorer]").forEach(init);
  if (typeof document$ !== "undefined") document$.subscribe(start);
  else document.addEventListener("DOMContentLoaded", start);
})();
