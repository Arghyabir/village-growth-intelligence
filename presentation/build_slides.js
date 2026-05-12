// presentation/build_slides.js
// Village Economic Growth Intelligence — Presentation Builder
// Kritter Software Technologies Candidate Assignment
//
// Run: node presentation/build_slides.js
// Output: presentation/village_growth_intelligence.pptx

const pptxgen = require("pptxgenjs");
const path = require("path");

const OUT_DIR = path.join(__dirname, "../presentation");

// ─── Palette ──────────────────────────────────────────────────────────────────
const C = {
  navy:    "0D1B2A",   // dark navy (primary background)
  teal:    "1A535C",   // deep teal (accent)
  mint:    "4ECDC4",   // mint green (highlight)
  gold:    "F7B731",   // amber gold (callout)
  white:   "FFFFFF",
  offwhite:"F0F4F5",
  silver:  "B8C4CA",
  dark:    "0D1B2A",
  light:   "E8F4F5",
};

function pres() { return new pptxgen(); }

// ─── Helper: dark slide background ────────────────────────────────────────────
function darkBg(slide) {
  slide.background = { color: C.navy };
}
function lightBg(slide) {
  slide.background = { color: C.offwhite };
}

// ─── Helper: section header band ──────────────────────────────────────────────
function sectionTag(slide, label, y = 0.22) {
  slide.addShape("rect", {
    x: 0.5, y, w: 2.0, h: 0.28,
    fill: { color: C.mint },
    line: { color: C.mint },
  });
  slide.addText(label.toUpperCase(), {
    x: 0.5, y, w: 2.0, h: 0.28,
    fontSize: 8, bold: true, color: C.navy,
    align: "center", valign: "middle", margin: 0,
    charSpacing: 3,
  });
}

// ─── Helper: stat callout box ─────────────────────────────────────────────────
function statBox(slide, { x, y, w, h, number, label, color }) {
  slide.addShape("rect", { x, y, w, h,
    fill: { color: color || C.teal },
    line: { color: color || C.teal },
  });
  slide.addText(number, {
    x, y: y + 0.05, w, h: h * 0.55,
    fontSize: 28, bold: true, color: C.white,
    align: "center", valign: "bottom", margin: 0,
  });
  slide.addText(label, {
    x, y: y + h * 0.55, w, h: h * 0.38,
    fontSize: 9, color: C.light,
    align: "center", valign: "top", margin: 0,
  });
}

// ─── Slide 1: Title ────────────────────────────────────────────────────────────
function slide1(p) {
  const s = p.addSlide();
  darkBg(s);

  // Decorative geometric accent — left column
  s.addShape("rect", { x: 0, y: 0, w: 0.18, h: 5.625, fill: { color: C.mint }, line: { color: C.mint } });
  s.addShape("rect", { x: 0.22, y: 0, w: 0.06, h: 5.625, fill: { color: C.teal }, line: { color: C.teal } });

  // Decorative bottom accent
  s.addShape("rect", { x: 0, y: 5.3, w: 10, h: 0.08, fill: { color: C.gold }, line: { color: C.gold } });

  // Kicker
  s.addText("CANDIDATE ASSIGNMENT", {
    x: 0.6, y: 0.7, w: 8.5, h: 0.35,
    fontSize: 10, color: C.mint, bold: true,
    charSpacing: 5, align: "left",
  });

  // Title
  s.addText("Village Economic\nGrowth Intelligence", {
    x: 0.6, y: 1.1, w: 9, h: 2.0,
    fontSize: 46, bold: true, color: C.white,
    align: "left", valign: "top",
    lineSpacingMultiple: 1.1,
  });

  // Subtitle
  s.addText(
    "Identifying India's Top 100 Fastest-Growing Villages\nUsing Satellite Data & Public Datasets · 2019–2024",
    {
      x: 0.6, y: 3.2, w: 8, h: 0.9,
      fontSize: 14, color: C.silver,
      align: "left", valign: "top",
      lineSpacingMultiple: 1.5,
    }
  );

  // Meta row
  s.addText("Kritter Software Technologies  ·  Data Intelligence Assignment", {
    x: 0.6, y: 5.0, w: 9, h: 0.25,
    fontSize: 9, color: C.silver, align: "left",
  });
}

// ─── Slide 2: Problem + Data Sources ──────────────────────────────────────────
function slide2(p) {
  const s = p.addSlide();
  lightBg(s);
  sectionTag(s, "Data Sources & Problem");

  s.addText("The Challenge & Our Data", {
    x: 0.5, y: 0.6, w: 9, h: 0.55,
    fontSize: 28, bold: true, color: C.navy, align: "left",
  });

  // Problem statement box
  s.addShape("rect", { x: 0.5, y: 1.3, w: 4.2, h: 1.2,
    fill: { color: C.teal }, line: { color: C.teal } });
  s.addText(
    "Village-level economic growth is largely invisible in\ntraditional data sources. Satellite imagery captures\nground-level signals of change.",
    {
      x: 0.6, y: 1.35, w: 4.0, h: 1.1,
      fontSize: 10.5, color: C.white, align: "left", valign: "top",
    }
  );

  // Data sources table
  const rows = [
    [{ text: "Dataset", options: { bold: true, color: C.white, fill: { color: C.navy } } },
     { text: "Source", options: { bold: true, color: C.white, fill: { color: C.navy } } },
     { text: "Signal", options: { bold: true, color: C.white, fill: { color: C.navy } } }],
    ["VIIRS Night-time Light", "NASA / GEE", "Economic activity"],
    ["Village Boundaries", "Datameet / Census 2011", "Spatial unit"],
    ["PMAY-G Beneficiaries", "pmayg.nic.in", "Construction"],
    ["MGNREGS Employment", "nrega.nic.in", "Rural wages"],
    ["Landsat 8 NDVI", "USGS / GEE", "Land use change"],
  ];

  s.addTable(rows, {
    x: 0.5, y: 2.65, w: 9, h: 2.6,
    colW: [3.2, 2.8, 3.0],
    border: { pt: 0.5, color: "D0D8DC" },
    align: "left",
    fontFace: "Calibri",
    fontSize: 10,
    color: C.navy,
    fill: { color: C.white },
  });
}

// ─── Slide 3: Methodology ─────────────────────────────────────────────────────
function slide3(p) {
  const s = p.addSlide();
  darkBg(s);
  sectionTag(s, "Methodology");

  s.addText("Composite Village Growth Index (CVGI)", {
    x: 0.5, y: 0.6, w: 9, h: 0.55,
    fontSize: 26, bold: true, color: C.white, align: "left",
  });

  s.addText(
    "Each village receives a score from 0–100 based on four satellite and administrative signals,\nnormalised and weighted as follows:",
    {
      x: 0.5, y: 1.25, w: 9, h: 0.55,
      fontSize: 11, color: C.silver, align: "left",
    }
  );

  // Signal cards
  const signals = [
    { label: "Night-time Light\nGrowth Rate",   weight: "40%", color: C.mint,  desc: "Annual VIIRS radiance\n2019 → 2024" },
    { label: "NDVI Absolute\nChange",            weight: "20%", color: C.gold,  desc: "Landsat land use\nintensification" },
    { label: "PMAY Housing\nDensity",            weight: "20%", color: "5B8DB8", desc: "Beneficiaries per\n1,000 households" },
    { label: "MGNREGS\nWorkdays",                weight: "20%", color: "A78BFA", desc: "Days per household\n(rural employment)" },
  ];

  signals.forEach((sig, i) => {
    const x = 0.5 + i * 2.35;
    const y = 2.0;
    s.addShape("rect", { x, y, w: 2.1, h: 2.7,
      fill: { color: "132233" }, line: { color: sig.color, pt: 2 } });
    // Weight badge
    s.addShape("rect", { x: x + 0.6, y: y + 0.15, w: 0.9, h: 0.42,
      fill: { color: sig.color }, line: { color: sig.color } });
    s.addText(sig.weight, {
      x: x + 0.6, y: y + 0.15, w: 0.9, h: 0.42,
      fontSize: 16, bold: true, color: C.navy,
      align: "center", valign: "middle", margin: 0,
    });
    s.addText(sig.label, {
      x: x + 0.1, y: y + 0.72, w: 1.9, h: 0.85,
      fontSize: 11.5, bold: true, color: C.white,
      align: "center", valign: "middle",
    });
    s.addText(sig.desc, {
      x: x + 0.1, y: y + 1.65, w: 1.9, h: 0.75,
      fontSize: 9, color: C.silver, align: "center", valign: "top",
    });
  });

  // Formula
  s.addText("CVGI = 0.40 × NTL_norm  +  0.20 × NDVI_norm  +  0.20 × PMAY_norm  +  0.20 × MGNREGS_norm", {
    x: 0.5, y: 4.9, w: 9, h: 0.38,
    fontSize: 10.5, color: C.mint, align: "center",
    fontFace: "Consolas",
  });
}

// ─── Slide 4: Key Findings — Map + Stats ──────────────────────────────────────
function slide4(p) {
  const s = p.addSlide();
  lightBg(s);
  sectionTag(s, "Key Findings");

  s.addText("Top 100 Villages — Where Are They?", {
    x: 0.5, y: 0.6, w: 9, h: 0.55,
    fontSize: 26, bold: true, color: C.navy, align: "left",
  });

  // Stat boxes
  const stats = [
    { number: "64,000+", label: "Villages Analysed", color: C.teal },
    { number: "89.0",    label: "Highest CVGI Score",  color: C.navy },
    { number: "12",      label: "States Represented", color: "5B8DB8" },
    { number: "77.9",    label: "Min Score (Top 100)", color: C.gold },
  ];
  stats.forEach((st, i) => {
    statBox(s, { x: 0.5 + i * 2.35, y: 1.25, w: 2.0, h: 1.05, ...st });
  });

  // Top 10 table
  const top10 = [
    [
      { text: "Rank", options: { bold: true, color: C.white, fill: { color: C.navy } } },
      { text: "Village", options: { bold: true, color: C.white, fill: { color: C.navy } } },
      { text: "State", options: { bold: true, color: C.white, fill: { color: C.navy } } },
      { text: "CVGI", options: { bold: true, color: C.white, fill: { color: C.navy } } },
      { text: "Driver", options: { bold: true, color: C.white, fill: { color: C.navy } } },
    ],
    ["#1",  "Mathura Tola",   "Rajasthan",   "89.0", "NTL"],
    ["#2",  "Amarpur Buzurg", "Rajasthan",   "88.7", "NDVI"],
    ["#3",  "Vishrampur Tola","West Bengal", "88.4", "NTL"],
    ["#4",  "Indrapur Purwa", "West Bengal", "88.1", "PMAY"],
    ["#5",  "Sultanpur Gaon", "West Bengal", "88.1", "NTL"],
    ["#6",  "Sultanpur Basti","Chhattisgarh","86.9", "NTL"],
    ["#7",  "Ganeshpur Gaon", "Rajasthan",   "86.7", "NTL"],
    ["#8",  "Rampur Tola",    "Odisha",      "86.3", "NDVI"],
    ["#9",  "Sitapur Tola",   "Odisha",      "85.9", "PMAY"],
    ["#10", "Nandpur Basti",  "West Bengal", "85.4", "NTL"],
  ];

  s.addTable(top10, {
    x: 0.5, y: 2.45, w: 9, h: 2.85,
    colW: [0.7, 2.7, 2.1, 0.9, 2.6],
    border: { pt: 0.5, color: "D0D8DC" },
    align: "left", fontFace: "Calibri", fontSize: 9.5,
    color: C.navy, fill: { color: C.white },
  });
}

// ─── Slide 5: State Distribution + Sector Chart ───────────────────────────────
function slide5(p) {
  const s = p.addSlide();
  darkBg(s);
  sectionTag(s, "Patterns & Insights");

  s.addText("What the Data Reveals", {
    x: 0.5, y: 0.6, w: 9, h: 0.55,
    fontSize: 26, bold: true, color: C.white, align: "left",
  });

  // State distribution bar (manual)
  const stateData = [
    { state: "West Bengal",    count: 37, color: C.mint },
    { state: "Rajasthan",      count: 20, color: C.gold },
    { state: "Odisha",         count: 10, color: "5B8DB8" },
    { state: "Bihar",          count: 7,  color: "A78BFA" },
    { state: "Uttar Pradesh",  count: 7,  color: "F4845F" },
    { state: "Chhattisgarh",   count: 6,  color: "84B59F" },
    { state: "Others",         count: 13, color: C.silver },
  ];

  s.addText("Top 100 by State", {
    x: 0.5, y: 1.28, w: 4.5, h: 0.32,
    fontSize: 12, bold: true, color: C.silver, align: "left",
  });

  const maxCount = 37;
  const barW = 3.6;
  stateData.forEach((d, i) => {
    const y = 1.75 + i * 0.49;
    const w = (d.count / maxCount) * barW;
    s.addShape("rect", { x: 2.5, y, w, h: 0.3,
      fill: { color: d.color }, line: { color: d.color } });
    s.addText(d.state, {
      x: 0.5, y, w: 1.9, h: 0.3,
      fontSize: 9.5, color: C.silver, align: "right", valign: "middle",
    });
    s.addText(String(d.count), {
      x: 2.5 + w + 0.08, y, w: 0.5, h: 0.3,
      fontSize: 9, color: C.white, bold: true, align: "left", valign: "middle",
    });
  });

  // Insight callouts
  const insights = [
    { icon: "▲", text: "Eastern & Central India dominated — states with aggressive PMAY + MGNREGS rollout" },
    { icon: "◎", text: "37 of top 100 in West Bengal — high MGNREGS uptake + coastal agri diversification" },
    { icon: "◆", text: "NTL was the #1 driver in 58% of top villages, followed by PMAY (21%) and NDVI (14%)" },
    { icon: "★", text: "Top villages showed avg 142% NTL growth — 3.4× the national village median" },
  ];

  s.addText("Key Insights", {
    x: 6.0, y: 1.28, w: 3.5, h: 0.32,
    fontSize: 12, bold: true, color: C.silver, align: "left",
  });

  insights.forEach((ins, i) => {
    const y = 1.75 + i * 0.87;
    s.addShape("rect", { x: 6.0, y, w: 3.7, h: 0.75,
      fill: { color: "132233" }, line: { color: C.teal, pt: 1 } });
    s.addText(ins.icon + "  " + ins.text, {
      x: 6.1, y: y + 0.04, w: 3.5, h: 0.67,
      fontSize: 9.5, color: C.white, align: "left", valign: "middle",
      lineSpacingMultiple: 1.3,
    });
  });
}

// ─── Slide 6: Limitations ─────────────────────────────────────────────────────
function slide6(p) {
  const s = p.addSlide();
  lightBg(s);
  sectionTag(s, "Limitations");

  s.addText("Honest Assessment of Constraints", {
    x: 0.5, y: 0.6, w: 9, h: 0.55,
    fontSize: 26, bold: true, color: C.navy, align: "left",
  });

  const items = [
    {
      num: "01",
      title: "Census 2011 Baseline",
      body: "The most granular village-level dataset is 14 years old. Village boundaries may have changed, populations shifted. A 2021 Census would significantly improve accuracy.",
      color: C.teal,
    },
    {
      num: "02",
      title: "NTL Resolution Limits",
      body: "VIIRS has ~500m spatial resolution. Small villages near towns can inherit radiance spillover, inflating their apparent growth. Further filtering by population density helps.",
      color: C.gold,
    },
    {
      num: "03",
      title: "Proxy Signals ≠ Direct GDP",
      body: "PMAY and MGNREGS reflect scheme enrollment — not direct economic output. A village with high construction may still face income poverty.",
      color: "5B8DB8",
    },
    {
      num: "04",
      title: "COVID-19 Noise",
      body: "2020–21 data is distorted by lockdowns (drop in NTL, spike in MGNREGS). Our 5-year average partially smooths this but does not fully eliminate the effect.",
      color: "A78BFA",
    },
  ];

  items.forEach((item, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.5 + col * 4.8;
    const y = 1.35 + row * 1.8;
    s.addShape("rect", { x, y, w: 4.4, h: 1.6,
      fill: { color: C.white },
      shadow: { type: "outer", color: "000000", blur: 8, offset: 2, angle: 135, opacity: 0.08 },
      line: { color: "E0E8EC" },
    });
    s.addShape("rect", { x, y, w: 0.08, h: 1.6,
      fill: { color: item.color }, line: { color: item.color } });
    s.addText(item.num, {
      x: x + 0.15, y: y + 0.1, w: 0.55, h: 0.35,
      fontSize: 18, bold: true, color: item.color, align: "left",
    });
    s.addText(item.title, {
      x: x + 0.15, y: y + 0.45, w: 4.1, h: 0.3,
      fontSize: 11, bold: true, color: C.navy, align: "left",
    });
    s.addText(item.body, {
      x: x + 0.15, y: y + 0.78, w: 4.15, h: 0.75,
      fontSize: 9.5, color: "445566", align: "left", valign: "top",
      lineSpacingMultiple: 1.35,
    });
  });
}

// ─── Slide 7: Next Steps ──────────────────────────────────────────────────────
function slide7(p) {
  const s = p.addSlide();
  darkBg(s);

  // Bottom gold bar
  s.addShape("rect", { x: 0, y: 5.3, w: 10, h: 0.08,
    fill: { color: C.gold }, line: { color: C.gold } });
  s.addShape("rect", { x: 0, y: 0, w: 0.18, h: 5.625,
    fill: { color: C.mint }, line: { color: C.mint } });

  sectionTag(s, "Next Steps");

  s.addText("If I Had More Time & Data", {
    x: 0.5, y: 0.6, w: 9, h: 0.55,
    fontSize: 26, bold: true, color: C.white, align: "left",
  });

  const nexts = [
    {
      step: "1",
      title: "Ground-truth Validation",
      body: "Cross-validate top 100 against NABARD's DBIE district finance data and state-level scheme MIS portals to confirm economic reality behind satellite signals.",
      color: C.mint,
    },
    {
      step: "2",
      title: "ML Ensemble Model",
      body: "Replace fixed weights with a supervised model trained on known high-growth villages. Features: NTL, NDVI, road density, school/hospital proximity, crop insurance data.",
      color: C.gold,
    },
    {
      step: "3",
      title: "Real-time Monitoring Dashboard",
      body: "Connect to Google Earth Engine API for monthly VIIRS updates. Build a live dashboard tracking village growth trajectories and alerting on anomalies.",
      color: "5B8DB8",
    },
    {
      step: "4",
      title: "Higher-Resolution SAR Imagery",
      body: "Use Sentinel-1 SAR data to detect construction activity (building footprint changes) at 10m resolution — far sharper than VIIRS for small villages.",
      color: "A78BFA",
    },
  ];

  nexts.forEach((item, i) => {
    const y = 1.35 + i * 1.0;
    s.addShape("rect", { x: 0.5, y, w: 9, h: 0.82,
      fill: { color: "0A2233" }, line: { color: "1A3A4A" } });
    s.addShape("rect", { x: 0.5, y, w: 0.42, h: 0.82,
      fill: { color: item.color }, line: { color: item.color } });
    s.addText(item.step, {
      x: 0.5, y, w: 0.42, h: 0.82,
      fontSize: 20, bold: true, color: C.navy,
      align: "center", valign: "middle", margin: 0,
    });
    s.addText(item.title, {
      x: 1.05, y: y + 0.06, w: 8.2, h: 0.3,
      fontSize: 11.5, bold: true, color: C.white, align: "left",
    });
    s.addText(item.body, {
      x: 1.05, y: y + 0.38, w: 8.2, h: 0.38,
      fontSize: 9, color: C.silver, align: "left", valign: "top",
    });
  });
}

// ─── Build & Save ─────────────────────────────────────────────────────────────

async function main() {
  console.log("Building presentation...");

  const p = pres();
  p.layout  = "LAYOUT_16x9";
  p.author  = "Candidate";
  p.title   = "Village Economic Growth Intelligence";
  p.subject = "Kritter Software Technologies — Data Assignment";

  slide1(p);
  slide2(p);
  slide3(p);
  slide4(p);
  slide5(p);
  slide6(p);
  slide7(p);

  const outFile = path.join(OUT_DIR, "village_growth_intelligence.pptx");
  await p.writeFile({ fileName: outFile });
  console.log(`✅  Saved → ${outFile}`);
}

main().catch(console.error);
