(() => {
  const STORAGE_KEYS = {
    darkMode: "fandomslang_dark_mode",
    history: "fandomslang_history",
  };

  function $(selector, root = document) {
    return root.querySelector(selector);
  }

  function $all(selector, root = document) {
    return Array.prototype.slice.call(root.querySelectorAll(selector));
  }

  function loadJson(key, fallback) {
    try {
      const raw = window.localStorage.getItem(key);
      if (!raw) return fallback;
      return JSON.parse(raw);
    } catch {
      return fallback;
    }
  }

  function saveJson(key, value) {
    try {
      window.localStorage.setItem(key, JSON.stringify(value));
    } catch {
      // ignore
    }
  }

  // Dark mode
  function initDarkMode() {
    const toggle = $("#darkModeToggle");
    if (!toggle) return;

    const stored = loadJson(STORAGE_KEYS.darkMode, null);
    if (stored === true) {
      document.body.classList.add("dark");
      toggle.checked = true;
    } else if (stored === false) {
      document.body.classList.remove("dark");
      toggle.checked = false;
    }

    toggle.addEventListener("change", () => {
      const enabled = toggle.checked;
      document.body.classList.toggle("dark", enabled);
      saveJson(STORAGE_KEYS.darkMode, enabled);
    });
  }

  // Copy helpers
  async function copyText(text) {
    if (!text) return;
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(text);
        return;
      }
    } catch {
      // fall through to manual method
    }

    const textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.setAttribute("readonly", "");
    textarea.style.position = "absolute";
    textarea.style.left = "-9999px";
    document.body.appendChild(textarea);
    textarea.select();
    try {
      document.execCommand("copy");
    } catch {
      // ignore
    }
    document.body.removeChild(textarea);
  }

  function initCopyButtons() {
    const container = $("#decodeResults");
    if (!container) return;

    const cards = $all(".card-result", container);
    $all(".copy-decoded", container).forEach((btn) => {
      btn.addEventListener("click", () => {
        const card = btn.closest(".card-result");
        if (!card) return;
        const decoded = card.getAttribute("data-decoded") || "";
        copyText(decoded);
      });
    });

    $all(".copy-share", container).forEach((btn, index) => {
      btn.addEventListener("click", () => {
        const card = btn.closest(".card-result");
        if (!card) return;
        const decoded = card.getAttribute("data-decoded") || "";
        const shareText =
          'Decoded via FandomSlang Decoder (Text ' +
          (index + 1) +
          '): ' +
          decoded;
        copyText(shareText);
      });
    });
  }

  // History
  function buildHistoryEntry(card, fandomKey) {
    const original = card.getAttribute("data-original") || "";
    const decoded = card.getAttribute("data-decoded") || "";
    const snippet =
      original.length > 120 ? original.slice(0, 117) + "..." : original;

    return {
      fandom: fandomKey,
      originalSnippet: snippet,
      decoded,
      createdAt: Date.now(),
    };
  }

  function renderHistory(listEl, items) {
    if (!listEl) return;
    listEl.innerHTML = "";
    if (!items || items.length === 0) {
      const p = document.createElement("p");
      p.className = "muted";
      p.textContent = "No decodes yet this session.";
      listEl.appendChild(p);
      return;
    }

    items.forEach((item) => {
      const card = document.createElement("article");
      card.className = "card card-history";

      const header = document.createElement("header");
      header.className = "card-history-header";

      const title = document.createElement("h3");
      title.textContent = "Fandom: " + item.fandom;
      header.appendChild(title);

      card.appendChild(header);

      const originalP = document.createElement("p");
      originalP.className = "history-original";
      originalP.textContent = item.originalSnippet;
      card.appendChild(originalP);

      const decodedP = document.createElement("p");
      decodedP.className = "history-decoded";
      decodedP.textContent = item.decoded;
      card.appendChild(decodedP);

      listEl.appendChild(card);
    });
  }

  function initHistory() {
    const historyList = $("#historyList");
    if (!historyList) return;

    let history = loadJson(STORAGE_KEYS.history, []);
    renderHistory(historyList, history);

    const container = $("#decodeResults");
    if (!container) return;

    const fandomKey = container.getAttribute("data-fandom") || "general";
    const cards = $all(".card-result", container);
    if (!cards.length) return;

    const newEntries = cards.map((card) => buildHistoryEntry(card, fandomKey));

    history = newEntries
      .concat(history)
      .sort((a, b) => b.createdAt - a.createdAt)
      .slice(0, 5);

    saveJson(STORAGE_KEYS.history, history);
    renderHistory(historyList, history);
  }

  document.addEventListener("DOMContentLoaded", () => {
    initDarkMode();
    initCopyButtons();
    initHistory();
  });
})();

