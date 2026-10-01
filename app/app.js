/* Aleida · menú interactivo — Code Consulting */

const DISHES = [
  {
    id: "hot-cakes", course: 1, name: "Hot cakes", price: 70,
    desc: "3 piezas acompañados de fresas, blue berries, mantequilla y miel.",
    model: "models/burger.glb",
    thumb: "img/dish-hotcakes.webp", realPhoto: true,
  },
  {
    id: "omelette-aleida", course: 1, name: "Omelette Aleida", price: 80,
    desc: "Queso de cabra, jamón serrano y espinacas.",
    model: "models/taco.glb",
    thumb: "img/dish-omelette-aleida.webp", stockPhoto: true,
  },
  {
    id: "omelette", course: 1, name: "Omelette", price: 70,
    desc: "Queso mozzarella, tomates cherry y espinacas.",
    model: "models/hotdog.glb",
    thumb: "img/dish-omelette.webp", stockPhoto: true,
  },
  {
    id: "huevos-al-gusto", course: 1, name: "Huevos al gusto", price: 75,
    desc: "Jamón, longaniza, chorizo, a la mexicana o estrellados.",
    model: "models/egg.glb",
    thumb: "img/dish-huevos-al-gusto.webp", stockPhoto: true,
  },
  {
    id: "huevos-motulenos", course: 1, name: "Huevos Motuleños", price: 85,
    desc: "Tostada con frijol refrito y huevo estrellado, bañados en salsa de tomate con chícharos y jamón, acompañados de plátano macho frito.",
    model: "models/whole-ham.glb",
    thumb: "img/dish-huevos-motulenos.webp", stockPhoto: true,
  },
  {
    id: "chilaquiles", course: 1, name: "Chilaquiles", price: 75,
    desc: "Verdes, rojos o de mole. Con huevo $75 · con pollo $80.",
    model: "models/cheese-cut.glb",
    thumb: "img/dish-chilaquiles.webp", realPhoto: true,
  },
  {
    id: "pan-dulce", course: 1, name: "Variedad de pan dulce", price: 15,
    desc: "Selección del día.",
    model: "models/cupcake.glb",
    thumb: "img/dish-pan-dulce.webp", stockPhoto: true,
  },
  {
    id: "fajitas", course: 2, name: "Fajitas de pollo", price: 140,
    desc: "Pechuga de pollo con cebolla y pimiento verde, con guarnición de frijol refrito y arroz.",
    model: "models/burger-cheese.glb",
    thumb: "img/dish-fajitas.webp", stockPhoto: true,
  },
  {
    id: "pechuga-empanizada", course: 2, name: "Pechuga de pollo empanizada", price: 145,
    desc: "Guarnición de frijol refrito y arroz.",
    model: "models/waffle.glb",
    thumb: "img/dish-pechuga-empanizada.webp", stockPhoto: true,
  },
  {
    id: "cordon-bleu", course: 2, name: "Pollo a la cordon bleu", price: 150,
    desc: "Pechuga de pollo empanizada rellena de jamón y queso, bañada en crema de champiñones, acompañada de ensalada de espinacas.",
    model: "models/cheese.glb",
    thumb: "img/dish-cordon-bleu.webp", stockPhoto: true,
  },
];

const STORE_KEY = "aleida.order.v1";
const $ = (id) => document.getElementById(id);

const mv = $("mv");
const scrim = $("scrim");
const detail = $("detail");
const orderPanel = $("order");

let order = read();
let activeDish = null;
let lastFocused = null;

function read() {
  try {
    const raw = localStorage.getItem(STORE_KEY);
    const parsed = raw ? JSON.parse(raw) : [];
    return Array.isArray(parsed) ? parsed.filter((id) => DISHES.some((d) => d.id === id)) : [];
  } catch {
    return [];
  }
}

function save() {
  try {
    localStorage.setItem(STORE_KEY, JSON.stringify(order));
  } catch {
    /* private mode — the order just won't survive a reload */
  }
}

const money = (n) => `$${n}`;
const dishById = (id) => DISHES.find((d) => d.id === id);

/* ---------- menu ---------- */

function renderMenu() {
  [1, 2].forEach((course) => {
    const list = $(`dishes-${course}`);
    const items = DISHES.filter((d) => d.course === course);
    list.replaceChildren(
      ...items.map((dish, i) => {
        const li = document.createElement("li");
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "dish";
        btn.style.setProperty("--i", i);
        btn.innerHTML = `
          <span class="dish__thumb-wrap">
            <img class="dish__thumb" src="${dish.thumb}" alt="" width="62" height="62" loading="lazy" decoding="async">
          </span>
          <span>
            <span class="dish__name">${dish.name}</span>
            <span class="dish__desc">${dish.desc}</span>
            <span class="dish__chip">${dish.realPhoto ? "Su foto · Ver en 3D" : "Ver en 3D"}</span>
          </span>
          <span class="dish__price">${money(dish.price)}</span>`;
        btn.addEventListener("click", () => openDetail(dish, btn));
        fadeInImage(btn.querySelector("img"));
        li.append(btn);
        return li;
      })
    );
  });
}

function fadeInImage(img) {
  if (img.complete) return;
  img.classList.add("is-pending");
  const reveal = () => img.classList.add("is-loaded");
  img.addEventListener("load", reveal, { once: true });
  img.addEventListener("error", reveal, { once: true });
}

/* ---------- panels ---------- */

function openPanel(panel) {
  lastFocused = document.activeElement;
  panel.hidden = false;
  scrim.hidden = false;
  requestAnimationFrame(() => {
    panel.classList.add("is-open");
    scrim.classList.add("is-open");
  });
  document.body.classList.add("is-locked");
  panel.querySelector(".panel__close").focus({ preventScroll: true });
}

function closePanel(panel) {
  panel.classList.remove("is-open");
  scrim.classList.remove("is-open");
  document.body.classList.remove("is-locked");
  window.setTimeout(() => {
    panel.hidden = true;
    scrim.hidden = true;
  }, 220);
  if (lastFocused) lastFocused.focus({ preventScroll: true });
}

function closeAny() {
  if (!detail.hidden) closePanel(detail);
  if (!orderPanel.hidden) closePanel(orderPanel);
}

/* ---------- dish detail ---------- */

function openDetail(dish, trigger) {
  activeDish = dish;
  lastFocused = trigger;

  $("detail-name").textContent = dish.name;
  $("detail-price").textContent = `${money(dish.price)} MXN`;
  $("detail-desc").textContent = dish.desc;
  $("viewer-error").hidden = true;
  $("ar-note").hidden = true;
  syncAddButton();

  mv.setAttribute("alt", `Modelo 3D de ${dish.name}`);
  mv.setAttribute("poster", dish.thumb);
  mv.src = dish.model;

  openPanel(detail);
}

mv.addEventListener("progress", (event) => {
  const bar = document.querySelector(".viewer__progress");
  const pct = event.detail.totalProgress;
  bar.style.width = `${pct * 100}%`;
  bar.style.opacity = pct < 1 ? "1" : "0";
});

mv.addEventListener("load", () => {
  $("viewer-error").hidden = true;
  // canActivateAR settles a beat after the model is ready
  window.setTimeout(() => {
    const note = $("ar-note");
    if (mv.canActivateAR) {
      note.hidden = true;
    } else {
      note.textContent = "Ábrelo desde tu celular para colocar el platillo en tu mesa.";
      note.hidden = false;
    }
  }, 350);
});

mv.addEventListener("error", () => {
  $("viewer-error").hidden = false;
});

// AR can fail after the session is handed off — without this the phone just sits
// on a black screen with no idea what went wrong
mv.addEventListener("ar-status", (event) => {
  const note = $("ar-note");
  const status = event.detail.status;
  if (status === "failed") {
    note.textContent =
      "Tu teléfono no pudo abrir la cámara en AR. Suele ser porque falta " +
      "«Servicios de Google Play para RA» o el navegador no tiene permiso de cámara. " +
      "El platillo se sigue viendo en 3D aquí.";
    note.hidden = false;
  } else if (status === "session-started" || status === "object-placed") {
    note.hidden = true;
  }
});

$("retry").addEventListener("click", () => {
  if (!activeDish) return;
  $("viewer-error").hidden = true;
  mv.src = "";
  mv.src = activeDish.model;
});

/* ---------- order ---------- */

function syncAddButton() {
  const btn = $("add-btn");
  const added = order.includes(activeDish.id);
  btn.textContent = added ? "Quitar de mi pedido" : "Agregar a mi pedido";
  btn.dataset.added = String(added);
}

function renderOrderBar() {
  const bar = $("order-bar");
  bar.hidden = order.length === 0;
  $("order-count").textContent = String(order.length);
}

function renderOrderPanel() {
  const list = $("order-list");
  const total = order.reduce((sum, id) => sum + (dishById(id)?.price ?? 0), 0);

  list.replaceChildren(
    ...order.map((id) => {
      const dish = dishById(id);
      const li = document.createElement("li");
      li.className = "order-item";
      li.innerHTML = `
        <span>${dish.name}</span>
        <span class="order-item__price">${money(dish.price)}</span>`;
      const remove = document.createElement("button");
      remove.type = "button";
      remove.className = "order-item__remove";
      remove.textContent = "Quitar";
      remove.addEventListener("click", () => {
        order = order.filter((x) => x !== id);
        save();
        renderOrderBar();
        renderOrderPanel();
        if (activeDish) syncAddButton();
      });
      li.append(remove);
      return li;
    })
  );

  $("order-empty").hidden = order.length > 0;
  $("order-total").hidden = order.length === 0;
  $("order-total-value").textContent = `${money(total)} MXN`;
}

$("add-btn").addEventListener("click", () => {
  if (!activeDish) return;
  order = order.includes(activeDish.id)
    ? order.filter((x) => x !== activeDish.id)
    : [...order, activeDish.id];
  save();
  syncAddButton();
  renderOrderBar();
});

$("order-bar").addEventListener("click", () => {
  renderOrderPanel();
  openPanel(orderPanel);
});

$("order-clear").addEventListener("click", () => {
  order = [];
  save();
  renderOrderBar();
  renderOrderPanel();
  if (activeDish) syncAddButton();
  closePanel(orderPanel);
});

/* ---------- wiring ---------- */

$("detail-close").addEventListener("click", () => closePanel(detail));
$("order-close").addEventListener("click", () => closePanel(orderPanel));
scrim.addEventListener("click", closeAny);

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") closeAny();
});

renderMenu();
renderOrderBar();
